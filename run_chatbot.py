import scallopy
import scallopy_ext
import os


SCALLOP_FILE = os.path.abspath(os.path.join(__file__, "../chatbot.scl"))


class Args:
    def __init__(self):
        self.cuda = False
        self.gpu = None
        self.num_allowed_openai_request = 5
        self.openai_gpt_model = "gpt-3.5-turbo"
        self.openai_gpt_temperature = 0
        self.clip_model_checkpoint = None
        self.save_image_path = None


# probably easier + faster + more efficient to use the same context repeatedly
# stores memoization of questions + documents and also saves money
# by not re-embedding documents each time
def process_question(conversation, question, qid):
    registry = scallopy_ext.PluginRegistry()
    registry.configure(args=Args().__dict__, unknown_args=None)

    ctx = scallopy.ScallopContext(provenance="unit")
    registry.load_into_ctx(ctx)
    ctx.import_file(SCALLOP_FILE)

    ctx.add_facts("conversation", [(conversation,)])
    ctx.add_facts("questions", [(qid, question)])
    ctx.run()
    out = list(ctx.relation('responses'))[0][1]

    return out


def main():
    conversation = ""
    qid = 0
    while True:
        question = input("Ask a question: ")
        if len(question) >= 1:
            qid += 1
            response = process_question(conversation, question, qid)
            print("Response:       " + response)
            conversation += question + "\n" + response + "\n"


if __name__ == "__main__":
    main()