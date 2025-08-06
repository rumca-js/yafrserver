from ..sqlmodel import ConfigurationEntry

class ConfigurationEntryController(object):
    def __init__(self, db, session=None):
        self.conn = db
        self.session = session

    def get_session(self):
        if not self.session:
            return self.conn.get_session()
        else:
            return self.session

    def get(self):
        Session = self.get_session()
        with Session() as session:
            return session.query(ConfigurationEntry).first()
