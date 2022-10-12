import json
import uuid

import docker as docker_lib
import grpc
import grpcbigbuffer as grpcbf
import pymongo
from bson.objectid import ObjectId
from google.protobuf.json_format import MessageToJson

from iobigdata import IOBigData
from protos import celaut_pb2, celaut_pb2 as celaut, gateway_pb2, gateway_pb2_grpc
from src.builder import build
from src.manager.payment_process import __check_payment_process
from src.manager.system_cache import Client, SystemCache
from src.utils import logger as l
from src.utils.utils import generate_uris_by_peer_id, get_network_name, \
    is_peer_available, to_gas_amount, \
    get_service_hex_main_hash

db = pymongo.MongoClient(
    "mongodb://localhost:27017/"
)["mongo"]["serviceInstances"]

# TODO get from enviroment variables.

DOCKER_CLIENT = lambda: docker_lib.from_env()
DEFAULT_SYSTEM_RESOURCES = celaut_pb2.Sysresources(
    mem_limit=50 * pow(10, 6),
)

DOCKER_NETWORK = 'docker0'
LOCAL_NETWORK = 'lo'

DEFAULT_INITIAL_GAS_AMOUNT_FACTOR = l.GET_ENV(env='DEFAULT_INITIAL_GAS_AMOUNT_FACTOR',
                                              default=1 / pow(10, 6))  # Percentage of the parent's gas amount.
USE_DEFAULT_INITIAL_GAS_AMOUNT_FACTOR = l.GET_ENV(env='USE_DEFAULT_INITIAL_GAS_AMOUNT_FACTOR',
                                                  default=False)  # Use DEFAULT_INITIAL_GAS_AMOUNT_FACTOR to calculate the initial gas amount.
DEFAULT_INTIAL_GAS_AMOUNT = l.GET_ENV(env='DEFAULT_INTIAL_GAS_AMOUNT', default=pow(10, 9))
COMPUTE_POWER_RATE = l.GET_ENV(env='COMPUTE_POWER_RATE', default=2)
COST_OF_BUILD = l.GET_ENV(env='COST_OF_BUILD', default=5)
EXECUTION_BENEFIT = l.GET_ENV(env='EXECUTION_BENEFIT', default=1)
MANAGER_ITERATION_TIME = l.GET_ENV(env='MANAGER_ITERATION_TIME', default=10)
TIME_TO_PRUNE_ZERO_CLIENT = l.GET_ENV(env='TIME_TO_PRUNE_ZERO_CLIENT', default=540)
MEMORY_LIMIT_COST_FACTOR = l.GET_ENV(env='MEMORY_LIMIT_COST_FACTOR', default=1 / pow(10, 6))
MIN_DEPOSIT_PEER = l.GET_ENV(env='MIN_PEER_DEPOSIT', default=pow(10, 64))
INITIAL_PEER_DEPOSIT_FACTOR = l.GET_ENV(env='INITIAL_PEER_DEPOSIT_FACTOR', default=0.5)
COST_AVERAGE_VARIATION = l.GET_ENV(env='COST_AVERAGE_VARIATION', default=1)
GAS_COST_FACTOR = l.GET_ENV(env='GAS_COST_FACTOR',
                            default=1)  # Applied only outside the manager. (not in maintain_cost)
MODIFY_SERVICE_SYSTEM_RESOURCES_COST = l.GET_ENV(env='MODIFY_SERVICE_SYSTEM_RESOURCES_COST_FACTOR', default=1)
ALLOW_GAS_DEBT = l.GET_ENV(env='ALLOW_GAS_DEBT', default=False)  # Could be used with the reputation system.
COMMUNICATION_ATTEMPTS = l.GET_ENV(env='COMMUNICATION_ATTEMPTS', default=1)
COMMUNICATION_ATTEMPTS_DELAY = l.GET_ENV(env='COMMUNICATION_ATTEMPTS_DELAY', default=60)
MIN_SLOTS_OPEN_PER_PEER = l.GET_ENV(env='MIN_SLOTS_OPEN_PER_PEER', default=1)
CLIENT_EXPIRATION_TIME = l.GET_ENV(env='CLIENT_EXPIRATION_TIME', default=1200)
CLIENT_MIN_GAS_AMOUNT_TO_RESET_EXPIRATION_TIME = l.GET_ENV(env='CLIENT_MIN_GAS_AMOUNT_TO_RESET_EXPIRATION_TIME',
                                                           default=pow(10, 3))

MEMSWAP_FACTOR = 0  # 0 - 1

sc = SystemCache()

# CONTAINER CACHE

# Insert the instance if it does not exists.
def insert_instance_on_mongo(instance: gateway_pb2.Instance, id: str = None) -> str:
    parsed_instance = json.loads(MessageToJson(instance))
    l.LOGGER('Inserting instance on mongo: ' + str(parsed_instance))

    result = pymongo.MongoClient(
        "mongodb://localhost:27017/"
    )["mongo"]["peerInstances"].update_one(
        {'_id': ObjectId(id)},
        {'$set': parsed_instance}
    ) if id else pymongo.MongoClient(
        "mongodb://localhost:27017/"
    )["mongo"]["peerInstances"].insert_one(parsed_instance)

    if not result.acknowledged:
        raise Exception('Could not insert instance on mongo.')

    return id if id else str(result.inserted_id)



def get_token_by_uri(uri: str) -> str:
    try:
        return sc.cache_service_perspective[uri]
    except Exception as e:
        l.LOGGER('EXCEPTION NO CONTROLADA. ESTO NO DEBERÍA HABER OCURRIDO ' + str(e) + ' ' + str(
            sc.cache_service_perspective) + ' ' + str(uri))  # TODO. Study the imposibility of that.
        raise e


def __push_token(token: str):
    with sc.cache_locks.lock(token): sc.system_cache[token] = {"mem_limit": 0}


def __modify_sysreq(token: str, sys_req: celaut_pb2.Sysresources) -> bool:
    if token not in sc.system_cache.keys(): raise Exception('Manager error: token ' + token + ' does not exists.')
    if sys_req.HasField('mem_limit'):
        variation = sc.system_cache[token]['mem_limit'] - sys_req.mem_limit

        if variation < 0:
            IOBigData().lock_ram(ram_amount=abs(variation))

        elif variation > 0:
            IOBigData().unlock_ram(ram_amount=variation)

        if variation != 0:
            with sc.cache_locks.lock(token): sc.system_cache[token]['mem_limit'] = sys_req.mem_limit

    return True


def __get_cointainer_by_token(token: str) -> docker_lib.models.containers.Container:
    return docker_lib.from_env().containers.get(
        container_id=token.split('##')[-1]
    )


def __refound_gas(
        gas: int = None,
        token: str = None,
        cache: dict = None,
        add_function=None,  # Lambda function if cache is not a dict of token:gas
) -> bool:
    try:
        with sc.cache_locks.lock(token):
            if add_function:
                add_function(gas)
            elif cache:
                cache[token] += gas
            else:
                raise Exception('Function usage error: Not add_function or cache provided.')
    except Exception as e:
        l.LOGGER('Manager error: ' + str(e))
        return False
    return True


# Only can be executed once.
def __refound_gas_function_factory(
        gas: int = None,
        cache: dict = None,
        token: str = None,
        container: list = None,
        add_function=None
) -> lambda: None:
    def use(l=[lambda: __refound_gas(gas=gas, cache=cache, token=token, add_function=add_function)]): l.pop()()

    if container: container.append(lambda: use())


def __increase_local_gas_for_client(client_id: str, amount: int) -> bool:
    l.LOGGER('Increase local gas for client ' + client_id + ' of ' + str(amount))
    if client_id not in sc.clients:  # TODO no debería de añadir un peer que no existe.
        raise Exception('Client ' + client_id + ' does not exists.')
    if not __refound_gas(
            gas=amount,
            add_function=lambda gas: sc.clients[client_id].add_gas(gas),
            token=client_id
    ):
        raise Exception('Manager error: cannot increase local gas for client ' + client_id + ' by ' + str(amount))
    return True


def __get_gas_amount_by_id(id: str) -> int:
    l.LOGGER('Get gas amount for ' + id)

    if id in sc.cache_service_perspective:
        return sc.system_cache[
            get_token_by_uri(uri=id)
        ]['gas']

    if id in sc.clients:
        return sc.clients[id].gas

    raise Exception('Manager error: ' + id + ' not found.')


def __get_gas_amount_by_ip(ip: str) -> int:
    return __get_gas_amount_by_id(id=ip)


def validate_payment_process(amount: int, ledger: str, contract: bytes, contract_addr: str, token: str) -> bool:
    return __check_payment_process(amount=amount, ledger=ledger, token=token, contract=contract,
                                   contract_addr=contract_addr) \
           and __increase_local_gas_for_client(client_id=token, amount=amount)  # TODO allow for containers too.


def spend_gas(
        token_or_container_ip: str,  # If its peer, the token is the peer id.
        #  If its a local service, the token could be the token or the container ip,
        #  on the last case, it take the token with cache service perspective.
        gas_to_spend: int,
        refund_gas_function_container: list = None
) -> bool:
    gas_to_spend = int(gas_to_spend)
    # l.LOGGER('Spend '+str(gas_to_spend)+' gas by ' + token_or_container_ip)
    try:
        # En caso de que sea un peer, el token es el peer id.
        if token_or_container_ip in sc.clients and (sc.clients[token_or_container_ip].gas >= gas_to_spend or ALLOW_GAS_DEBT):
            with sc.cache_locks.lock(token_or_container_ip):
                sc.clients[token_or_container_ip].reduce_gas(gas=gas_to_spend)
            __refound_gas_function_factory(
                gas=gas_to_spend,
                token=token_or_container_ip,
                add_function=lambda gas: sc.clients[token_or_container_ip].add_gas(gas),
                container=refund_gas_function_container
            )
            return True

        # En caso de que token_or_container_ip sea el token del contenedor.
        elif token_or_container_ip in sc.system_cache and (
                sc.system_cache[token_or_container_ip]['gas'] >= gas_to_spend or ALLOW_GAS_DEBT):
            with sc.cache_locks.lock(token_or_container_ip):
                sc.system_cache[token_or_container_ip]['gas'] -= gas_to_spend
            __refound_gas_function_factory(
                gas=gas_to_spend,
                cache=sc.system_cache,
                token=token_or_container_ip,
                container=refund_gas_function_container
            )
            return True

        # En caso de que token_or_container_ip sea la ip del contenedor.
        token_or_container_ip = sc.cache_service_perspective[token_or_container_ip]
        if token_or_container_ip in sc and (
                sc.system_cache[token_or_container_ip]['gas'] >= gas_to_spend or ALLOW_GAS_DEBT):
            with sc.cache_locks.lock(token_or_container_ip): sc.system_cache[token_or_container_ip]['gas'] -= gas_to_spend
            __refound_gas_function_factory(
                gas=gas_to_spend,
                cache=sc.system_cache,
                token=token_or_container_ip,
                container=refund_gas_function_container
            )
            return True
    except Exception as e:
        l.LOGGER('Manager error spending gas ' + str(e) + ' ' + str(gas_to_spend) + ' ' + token_or_container_ip + \
                 '\n peer instances -> ' + str(sc.clients) + \
                 '\n system cache -> ' + str(sc) + \
                 '\n cache service perspective -> ' + str(sc.cache_service_perspective) + \
                 '\n        ----------------------\n\n\n')

    return False


def generate_client() -> gateway_pb2.Client:
    # No collisions expected.
    client_id = uuid.uuid4().hex
    sc.clients[client_id] = Client()
    l.LOGGER('New client created ' + client_id)
    return gateway_pb2.Client(
        client_id=client_id,
    )


def generate_client_id_in_other_peer(peer_id: str) -> str:
    if not is_peer_available(peer_id=peer_id, min_slots_open=MIN_SLOTS_OPEN_PER_PEER):
        l.LOGGER('Peer ' + peer_id + ' is not available.')
        raise Exception('Peer not available.')

    if peer_id not in sc.clients_on_other_peers:
        l.LOGGER('Generate new client for peer ' + peer_id)
        with sc.cache_locks.lock(peer_id):
            sc.clients_on_other_peers[peer_id] = str(next(grpcbf.client_grpc(
                method=gateway_pb2_grpc.GatewayStub(
                    grpc.insecure_channel(
                        next(generate_uris_by_peer_id(peer_id=peer_id))
                    )
                ).GenerateClient,
                indices_parser=gateway_pb2.Client,
                partitions_message_mode_parser=True
            )).client_id)

    return sc.clients_on_other_peers[peer_id]


def add_peer(
        peer_id: str
) -> bool:
    try:
        if peer_id not in sc.total_deposited_on_other_peers:
            with sc.cache_locks.lock(peer_id):
                sc.total_deposited_on_other_peers[peer_id] = 0

        l.LOGGER('Add peer ' + peer_id + ' with client ' +
                 generate_client_id_in_other_peer(peer_id=peer_id)
                 )
        return True
    except:
        return False


def default_initial_cost(
        father_id: str = None,
) -> int:
    l.LOGGER('Default cost for ' + (father_id if father_id else 'local'))
    return (int(__get_gas_amount_by_id(
        id=father_id) * DEFAULT_INITIAL_GAS_AMOUNT_FACTOR)) if father_id and USE_DEFAULT_INITIAL_GAS_AMOUNT_FACTOR else int(
        DEFAULT_INTIAL_GAS_AMOUNT)


def add_container(
        father_id: str,
        container: docker_lib.models.containers.Container,
        initial_gas_amount: int,
        system_requeriments_range: gateway_pb2.ModifyServiceSystemResourcesInput = None
) -> str:
    l.LOGGER('Add container for ' + father_id)
    token = father_id + '##' + container.attrs['NetworkSettings']['IPAddress'] + '##' + container.id
    if token in sc.system_cache.keys(): raise Exception('Manager error: ' + token + ' exists.')

    __push_token(token=token)
    sc.system_cache.__set_on_cache(
        agent_id=father_id,
        container_id___his_token_encrypt=container.id,
        container_ip___peer_id=container.attrs['NetworkSettings']['IPAddress'],
        container_id____his_token=token,
    )
    with sc.cache_locks.lock(token):
        sc.system_cache[token]['gas'] = initial_gas_amount if initial_gas_amount else default_initial_cost(
            father_id=father_id)
    if not container_modify_system_params(
            token=token,
            system_requeriments_range=system_requeriments_range
    ): raise Exception('Manager error adding ' + token + '.')
    return token


def container_modify_system_params(
        token: str,
        system_requeriments_range: gateway_pb2.ModifyServiceSystemResourcesInput = None
) -> bool:
    l.LOGGER('Modify params of ' + token)

    # https://docker-py.readthedocs.io/en/stable/containers.html#docker.models.containers.Container.update
    # Set system requeriments parameters.

    system_requeriments = system_requeriments_range.max_sysreq  # TODO implement the use of min_sysreq.
    if not system_requeriments: return False

    if __modify_sysreq(
            token=token,
            sys_req=system_requeriments
    ):
        try:
            # Memory limit should be smaller than already set memoryswap limit, update the memoryswap at the same time
            __get_cointainer_by_token(
                token=token
            ).update(
                mem_limit=system_requeriments.mem_limit if MEMSWAP_FACTOR == 0 \
                    else system_requeriments.mem_limit - MEMSWAP_FACTOR * system_requeriments.mem_limit,
                memswap_limit=system_requeriments.mem_limit if MEMSWAP_FACTOR > 0 else -1
            )
        except:
            return False
        return True

    return False


def could_ve_this_sysreq(sysreq: celaut_pb2.Sysresources) -> bool:
    return IOBigData().prevent_kill(len=sysreq.mem_limit)  # Prevent kill dice de lo que dispone actualmente libre.
    # It's not possible local, but other pair can, returns True.


def get_sysresources(token: str) -> gateway_pb2.ModifyServiceSystemResourcesOutput:
    return gateway_pb2.ModifyServiceSystemResourcesOutput(
        sysreq=celaut_pb2.Sysresources(
            mem_limit=sc.system_cache[token]["mem_limit"],
        ),
        gas=to_gas_amount(
            gas_amount=sc.system_cache[token]["gas"]
        )
    )


# PRUNE CONTAINER METHOD

def prune_container(token: str) -> int:
    l.LOGGER('Prune container ' + token)
    if get_network_name(ip_or_uri=token.split('##')[
        1]) == DOCKER_NETWORK:  # Suponemos que no tenemos un token externo que empieza por una direccion de nuestra subnet.
        try:
            refund = sc.purgue_internal(
                agent_id=token.split('##')[0],
                container_id=token.split('##')[2],
                container_ip=token.split('##')[1],
                token=token
            )
        except Exception as e:
            l.LOGGER('Error purging ' + token + ' ' + str(e))
            return False

    else:
        try:
            refund = sc.purgue_external(
                agent_id=token.split('##')[0],
                peer_id=token.split('##')[1],
                his_token=token.split('##')[2],
            )
        except Exception as e:
            l.LOGGER('Error purging ' + token + ' ' + str(e))
            return False

    # __refound_gas() # TODO refound gas to parent. Need to check what cache is. peer_instances or system_cache. Podría usar una variable de entorno para hacerlo o no.
    return refund



# COST FUNCTIONS

def maintain_cost(sysreq: dict) -> int:
    return MEMORY_LIMIT_COST_FACTOR * sysreq['mem_limit']


def build_cost(service_buffer: bytes, metadata: celaut.Any.Metadata) -> int:
    is_built = (get_service_hex_main_hash(service_buffer=service_buffer, metadata=metadata)
                in [img.tags[0].split('.')[0] for img in DOCKER_CLIENT().images.list()])
    if not is_built and \
            not build.check_supported_architecture(metadata=metadata): raise build.UnsupportedArquitectureException
    try:
        # Coste de construcción si no se posee el contenedor del servicio.
        # Debe de tener en cuenta el coste de buscar el conedor por la red.
        return sum([
            COST_OF_BUILD * (is_built is False),
            # Coste de obtener el contenedor ... #TODO
        ])
    except Exception as e:
        l.LOGGER('Manager - build cost exception: ' + str(e))
        pass
    return COST_OF_BUILD


def execution_cost(service_buffer: bytes, metadata: celaut.Any.Metadata) -> int:
    l.LOGGER('Get execution cost')
    try:
        return sum([
            len(DOCKER_CLIENT().containers.list()) * COMPUTE_POWER_RATE,
            build_cost(service_buffer=service_buffer, metadata=metadata),
            EXECUTION_BENEFIT
        ])
    except build.UnsupportedArquitectureException as e:
        raise e
    except Exception as e:
        l.LOGGER('Error calculating execution cost ' + str(e))
        raise e


def start_service_cost(
        metadata,
        service_buffer,
        initial_gas_amount: int
) -> int:
    return execution_cost(
        service_buffer=service_buffer,
        metadata=metadata
    ) + initial_gas_amount