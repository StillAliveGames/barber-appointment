from app import db
from app.models import User, Role, Master, Service

# Создаём пользователя с ролью мастера
master_user = User(username='ivan', email='ivan@barber.com')
master_user.set_password('master123')

master_role = Role.query.filter_by(name='master').first()
if master_role:
    master_user.roles.append(master_role)

db.session.add(master_user)
db.session.commit()
print(f"Создан пользователь мастер: {master_user.username}")

# Создаём профиль мастера
master = Master(user_id=master_user.id, specialty='Мужские стрижки, борода')
db.session.add(master)
db.session.commit()
print(f"Создан профиль мастера: {master.user.username}")

# Добавляем услуги
services = [
    Service(name='Мужская стрижка', price=800, duration=30),
    Service(name='Стрижка бороды', price=400, duration=20),
    Service(name='Отец и сын', price=1500, duration=60),
]
for s in services:
    db.session.add(s)
db.session.commit()
print("Услуги добавлены")

# Связываем мастера с услугами (первые две)
master.services.append(services[0])
master.services.append(services[1])
db.session.commit()
print("Мастер связан с услугами")

exit()