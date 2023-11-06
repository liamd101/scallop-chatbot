import scallopy
import scallopy_ext
import os


DOCUMENT_DIR = os.path.abspath(os.path.join(__file__, "../documents"))
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


def build_index(ctx):
    for idx, filename in enumerate(os.listdir(DOCUMENT_DIR)):
        rel_path = os.path.join(DOCUMENT_DIR, filename)
        ctx.add_facts('document_paths', [(idx, rel_path)])


def process_question(ctx, conversation, question, qid):
    ctx.add_facts("conversation", [(conversation,)])
    ctx.add_facts("questions", [(qid, question)])
    ctx.run()
    responses = list(ctx.relation('responses'))

    out = ''
    # prob a better way to do this
    for (new_q, response) in responses:
        if new_q == question:
            out = response
            break

    return out


def main():
    conversation = ""
    qid = 0

    registry = scallopy_ext.PluginRegistry()
    registry.configure(args=Args().__dict__, unknown_args=None)

    ctx = scallopy.ScallopContext(provenance="unit")
    registry.load_into_ctx(ctx)
    ctx.import_file(SCALLOP_FILE)

    build_index(ctx)
    while True:
        question = input("Ask a question: ")
        if len(question) >= 1:
            qid += 1
            response = process_question(ctx, conversation, question, qid)
            print("Response:       " + response)
            conversation += question + "\n" + response + "\n"


if __name__ == "__main__":
    main()
