import sqlite3
import spacy
from sklearn.metrics.pairwise import cosine_similarity

class MessageStore:
    __instance = None

    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
            cls.__instance.__initialize_database()
            cls.__instance.__load_embeddings()
        return cls.__instance

    def __initialize_database(self):
        self.conn = sqlite3.connect('messages.db')
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS messages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                role TEXT,
                content TEXT
            )
        ''')
        self.conn.commit()

    def __load_embeddings(self):
        self.nlp = spacy.load("es_core_news_lg")

    def __get_message_embeddings(self):
        self.cursor.execute('SELECT content FROM messages')
        rows = self.cursor.fetchall()
        embeddings = []
        for row in rows:
            doc = self.nlp(row[0])
            embedding = doc.vector
            embeddings.append(embedding)
        return embeddings

    def add_message(self, message):
        self.cursor.execute('INSERT INTO messages (role, content) VALUES (?, ?)', (message["role"], message["content"]))
        self.conn.commit()

    def get_messages(self):
        self.cursor.execute('SELECT role, content FROM messages')
        rows = self.cursor.fetchall()
        messages = []
        for row in rows:
            message = {"role": row[0], "content": row[1]}
            messages.append(message)
        return messages

    def get_relevant(self, text, num_results=5, similarity_threshold=0.7):
        input_doc = self.nlp(text)
        input_embedding = input_doc.vector

        message_embeddings = self.__get_message_embeddings()

        similarities = cosine_similarity([input_embedding], message_embeddings)
        similarity_scores = similarities[0]

        # Get indices of messages with similarity scores greater than or equal to the threshold
        similar_indices = [i for i, score in enumerate(similarity_scores) if score >= similarity_threshold]

        # Sort the indices based on similarity scores in descending order
        similar_indices = sorted(similar_indices, key=lambda i: similarity_scores[i], reverse=True)

        relevant_messages = []
        for index in similar_indices[:num_results]:
            message = self.get_messages()[index]
            similarity_index = similarity_scores[index]
            message_with_similarity = {
                "message": message,
                "similarity_index": similarity_index
            }
            relevant_messages.append(message_with_similarity)

        return relevant_messages
