from typing import Generator, List
from src.actions.__interface import table_command
from src.utils.utils import peers_id_iterator


def generator() -> Generator[List[str], None, None]:
    for peer in peers_id_iterator():
        yield [peer]


def peers(stream: bool = True):
    table_command(f=generator, headers=['PAR'], stream=stream)


def delete(peer_id: str):
    from src.database.query_interface import commit_query

    # TODO delete all the related data.
    commit_query(query='''
                            DELETE FROM peer
                            WHERE id = ?
                    ''', params=(peer_id,)
                 )

    print(f"Deleted {peer_id} peer")


def delete_all():
    [delete(_peer) for _peer in peers_id_iterator()]
