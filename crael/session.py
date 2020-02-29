import uuid
import datetime
import pickle
import logging as logger


class SessionHandler:
    def __init__(self):
        self._sessions = dict()

    def __repr__(self):
        return f"Active sessions:\n{self._sessions.keys}"

    def start_session(self, session_id, overight=False):

        if not session_id:
            session_id = uuid.uuid4().hex

            if session_id in self._sessions.keys() and overight:
                self._sessions[session_id] = dict()
            else:
                logger.info(f"Session with {session_id} already exists")

        self._sessions[session_id] = {
            "start_time": datetime.datetime,
            "last_commit": None,
        }
        logger.info(f"Started a new Session with id: {session_id}")

    def session_add(self, session_id, key, value):
        session = self._sessions[session_id]
        try:
            session[key] = value
        except Exception as e:
            logger.error(f"Could not add content {e}")

    def commit_session(self, session_id):
        session = self._sessions[session_id]
        session["last_commit"] = datetime.datetime
        with open(self.session_id, "ab") as session_file:
            pickle.dump(self._content, session_file)
