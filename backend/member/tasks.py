from config import celery_app

# @celery_app.task(bind=True)
# def team_add(_, instance_id):
#     from member.models import Team
#     instance = Team.objects.get(id=instance_id)
#     instance.add_member(instance)