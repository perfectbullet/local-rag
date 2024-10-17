# 📚 Local RAG

![local-rag-demo](demo.gif)

[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/8588/badge)](https://www.bestpractices.dev/projects/8588)
![GitHub Commit Activity](https://img.shields.io/github/commit-activity/t/jonfairbanks/local-rag)
![GitHub Last Commit](https://img.shields.io/github/last-commit/jonfairbanks/local-rag)
![GitHub License](https://img.shields.io/github/license/jonfairbanks/local-rag)

Offline, Open-Source RAG

Ingest files for retrieval augmented generation (RAG) with open-source Large Language Models (LLMs), all without 3rd parties or sensitive data leaving your network.

Features:

- Offline Embeddings & LLMs Support (No OpenAI!)
- Support for Multiple Sources
    - Local Files
    - GitHub Repos
    - Websites
- Streaming Responses
- Conversational Memory
- Chat Export

Learn More:

- [Setup & Deploy the App](docs/setup.md)
- [Using Local RAG](docs/usage.md)
- [RAG Pipeline](docs/pipeline.md)
- [Planned Features](docs/todo.md)
- [Troubleshooting](docs/troubleshooting.md)
- [Known Bugs & Issues](docs/todo.md#known-issues--bugs)
- [Resources](docs/resources.md)
- [Contributing](docs/contributing.md)





# note of problems

Installing collected packages: pillow, pi_heif
  Attempting uninstall: pillow
    Found existing installation: Pillow 9.0.1
    Not uninstalling pillow at /usr/lib/python3/dist-packages, outside environment /home/zj/python-venvs/local-rag
    Can't uninstall 'Pillow'. No files were found to uninstall.
ERROR: pip's dependency resolver does not currently take into account all the packages that are installed. This behaviour is the source of the following dependency conflicts.
llama-index-readers-file 0.2.2 requires pypdf<5.0.0,>=4.0.1, but you have pypdf 5.0.1 which is incompatible.
Successfully installed pi_heif-0.18.0 pillow-10.4.0
(local-rag) zj@zj-desktop:~/local-rag/ddddddemo$ pip uninstall pypdf