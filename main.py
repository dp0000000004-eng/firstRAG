class RAGModel:

    def __init__(self, prompt="you name?"):
        self.prompt = prompt

    model = ...

    knowedge = [
        "deba is a good boy",
        "i forget my password",
        "the winter is comming"
    ]

    def vectore_db():
        return RAGModel.knowedge

    def prompt_vecs(self):
        p_vecs = RAGModel.model.encode(self.prompt)
        return p_vecs

    def db_vecs():
        knowedge_vecs = RAGModel.model.encode(RAGModel.vectore_db())
        return knowedge_vecs

    def score():
        # scores = util.cos_sim(q_vec, RAGModel.db_vecs())[0]
        return scores

    
#.


def main():
    while True:
        prompt = input('Promt: ')

        if prompt.lower() == "stop":
            break

        ...


call = RAGModel()
ans = call.prompt_vecs()
print(ans)