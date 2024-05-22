from .models import Message

class Common:
    def __init__(self) -> None:
        pass

    def users_list(self, user_id, user_org):
        query = '''WITH RankedMessages AS (
                    SELECT
                        mm.id,
                        mm.sender_id,
                        mm.receiver_id,
                        mm.content,
                        mm.date,
                        au.id AS user_id,
                        au.first_name,
                        au.last_name,
                        ee.profile,
                        ROW_NUMBER() OVER (PARTITION BY CASE WHEN mm.sender_id = %s THEN mm.receiver_id ELSE mm.sender_id END ORDER BY mm.date DESC) AS message_rank
                    FROM
                        message_message mm
                    LEFT JOIN
                        auth_user au ON au.id = case when mm.sender_id = %s then mm.receiver_id else mm.sender_id end
                    LEFT JOIN
                        employeedetails_employee ee ON ee.user_id = au.id
                    WHERE
                        mm.organization_id = %s
                        and mm.is_deleted = false
                        AND (mm.sender_id = %s OR mm.receiver_id = %s)
                )
                SELECT
                    id,
                    user_id,
                    sender_id,
                    receiver_id,
                    content,
                    date,
                    profile,
                    first_name,
                    last_name
                FROM
                    RankedMessages
                WHERE
                    message_rank = 1
                order by date desc
                '''
        parameters = []
        parameters.extend([user_id, user_id, user_org, user_id, user_id])
        result = Message.objects.raw(query, parameters)
        return result