import uuid

def random_suffix():
    return uuid.uuid4().hex[:6]

def random_team_name(name=''):
    return f'team-{name}-{random_suffix()}'
