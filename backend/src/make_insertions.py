from datetime import timedelta

from sqlalchemy import insert

from database import SessionLocal
from turn.models import QueueLifetime, QueueRole, QueueAction


con = SessionLocal()

def insertions_for_queue_lifetimes():
    print('\nStart insertions into `QueueLifetime` ...')
    
    con.execute(
        insert(QueueLifetime),
        [
            {
                'key': 'QL00001',
                'lifetime': timedelta(minutes=45)
            },
            {
                'key': 'QL00002',
                'lifetime': timedelta(hours=1, minutes=45)
            },
            {
                'key': 'QL00003',
                'lifetime': timedelta(hours=3)
            },
            {
                'key': 'QL00004',
                'lifetime': timedelta(hours=8)
            },
        ]
    )
    con.commit()

    print('Complete insertions!')

def insertions_for_queue_roles():
    print('\nStart insertions into `QueueRole` ...')

    con.execute(
        insert(QueueRole),
        [
            {
                'key': 'QR00001',
                'role': 'not_member',
                'detail': 'The not member of group'
            },
            {
                'key': 'QR00002',
                'role': 'member',
                'detail': 'The member of group'
            },
            {
                'key': 'QR00003',
                'role': 'lead',
                'detail': 'The leader of group'
            },
        ]
    )
    con.commit()

    print('Complete insertions!')

def insertions_for_queue_actions():
    print('\nStart insertions into `QueueAction` ...')

    con.execute(
        insert(QueueAction),
        [
            {
                'key': 'QA00001',
                'action': 'create',
                'detail': 'The user $1 created new queue $2.',
            },
            {
                'key': 'QA00002',
                'action': 'delete',
                'detail': 'The user $1 delete queue $2.',
            },
            {
                'key': 'QA00003',
                'action': 'connect',
                'detail': 'The user $1 connected to the channel.',
            },
            {
                'key': 'QA00004',
                'action': 'disconnect',
                'detail': 'The user $1 disconnected from the channel.',
            },
            {
                'key': 'QA00005',
                'action': 'join',
                'detail': 'The user $1 joined to the queue $1.',
            },
            {
                'key': 'QA00006',
                'action': 'leave',
                'detail': 'The user $1 leaved from the queue $2.',
            },
            {
                'key': 'QA00007',
                # 'action': 'replace',
                'action': 'replace-offer',
                'detail': 'The user $1  suggested switching placeswith user $2.',
            },
            {
                'key': 'QA00008',
                'action': 'replace-accept',
                'detail': 'The user $1 accepted user $2 suggestions.',
            },
            {
                'key': 'QA00009',
                'action': 'skip',
                'detail': 'The user $1 skipped ahead to next user $2.',
            },
        ]
    )
    con.commit()

    print('Complete insertions!\n')


if __name__ == '__main__':
    print('Open database connection ...')

    insertions_for_queue_lifetimes()
    insertions_for_queue_roles()
    insertions_for_queue_actions()

    con.close()
    print('Close connection.')
