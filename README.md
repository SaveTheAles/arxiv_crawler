# ArXiv.org crawler for `cyber` network

This tool able you to make much more cyberlinks easier. You can move arxiv.org articles to the Great Web by relevant keywords. Thanks to [this](https://github.com/vgrabovets/multi_rake) keyword extractor.

The tool:

- parses articles metadata by keyword you interesting in
- gets the keywords from the article summary
- downloads the article in pdf
- calculates ipfs hashes from keywords, title and downloaded pdf
- pins all hashes to you machine
- generate the unsigned transaction type

```bash
[keywords_ipfs_hashes] - > article_ipfs_hash
```

## Disclaimer

This is a semi-automatic script. Work in progress and so far from ideal.

## Requirements

- Running [ipfs](https://docs.ipfs.io/guides/guides/install/) daemon v0.4.18 and higher
- [Cyberdcli](https://cybercongress.ai/docs/cyberd/ultimate-commands-guide/)
- [Python3](https://docs.python-guide.org/starting/installation/)

## Usage

Parsing arxiv and generating transactions:

1. Clone this repo and go into it

    ```bash
    git clone https://github.com/SaveTheAles/arxiv_crawler.git
    cd arxiv_crawler
    ```

2. Install python packages

    ```bash
    pip install pandas
    pip install arxiv
    pip install multi-rake
    pip install ipfshttpclient
    pip install progressbar
    pip install json
    ```

3. Fill `config.py`

    Put your `cyber` address as `ADDRESS` variable and `QUERY` variable as keyword you want to discover.

4. Run main.py

    ```bash
    python3 main.py
    ```

    As result of this command will be `./data/txs/link_txN.json` files with prepared for signing and broadcasting to `cyber` network

Sign and broadcast transactions. This step will use a simple bash script. It will work only if you allow you tx signing without a password. Otherwise, you should update it or sign transactions manually.

1. Make executable:

    ```bash
    chmod u+x sign-brod.sh
    ```

2. Define range for loop (from 0 till number of transactions) in `sign-brod.sh`

3. Insert the proxy node in `sign-brod.sh`

4. Run sign-brod.sh:

    ```bash
    ./sign-brod.sh
    ```

    You should see broadcasted transactions as output in console.

## ToDo

- Built-in signer and broadcaster
- Storage for saving state
- Checks for valid txs and bandwidth

## Contribution

Welcome. If you knows how to implement some or make the tool better do it for the Great Justice! Check the ToDo section and Wishlist for inspiration.

## Wishlist

Here you can add with PR all features you want. 