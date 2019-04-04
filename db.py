import peewee as pw
import datetime

db = pw.SqliteDatabase('stalkr.sqlite')

class BaseModel(pw.Model):
    class Meta:
        database = db

class User(BaseModel):
    username = pw.TextField(unique=True)
    password = pw.TextField()
    joined_date = pw.DateTimeField(default=datetime.date.today)

class S_Country(BaseModel):
    name = pw.TextField()

class S_City(BaseModel):
    name = pw.TextField()
    country = pw.ForeignKeyField(S_Country)

class S_School(BaseModel):
    full_name = pw.TextField()
    short_name = pw.TextField(null=True, unique=True)
    city = pw.ForeignKeyField(S_City)

class S_School_Course(BaseModel):
    name = pw.TextField()
    school = pw.ForeignKeyField(S_School)

class S_Sport(BaseModel):
    name = pw.TextField()

class S_Person(BaseModel):
    first_name = pw.TextField()
    last_name = pw.TextField()
    birthday = pw.DateField(null=True)
    city = pw.ForeignKeyField(S_City, null=True)
    nationality = pw.ForeignKeyField(S_Country, null=True)
    school = pw.ForeignKeyField(S_School, null=True)
    school_course = pw.ForeignKeyField(S_School_Course, null=True)
    gender = pw.IntegerField(default=3)
    wiki_page = pw.TextField(null=True)
    relationship_status = pw.IntegerField(default=0)
    sport = pw.ForeignKeyField(S_Sport, null=True)
    favorite_color = pw.TextField(null=True)
    deceased_date = pw.DateField(null=True)
    father = pw.DeferredForeignKey('s_person', null=True)
    mother = pw.DeferredForeignKey('s_person', null=True)
    is_hidden = pw.IntegerField(default=0)

    @property
    def full_name(self):
        if self.nationality and self.nationality.name == 'China':
            return self.last_name + ' ' + self.first_name
        else:
            return self.first_name + ' ' + self.last_name

class S_PersonRelationship(BaseModel):
    person1 = pw.ForeignKeyField(S_Person)
    person2 = pw.ForeignKeyField(S_Person)
    started = pw.DateField()
    ended = pw.DateField(null=True)
    
def init_db():
    db.create_tables([
        User, S_Country, S_City, S_School, S_School_Course, S_Sport,
        S_Person, S_PersonRelationship
        ])
