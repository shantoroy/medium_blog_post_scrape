"""
This program analyzes tags for relevant integrated post.
Analysis include:
1. Tag Frequency
2. Responses (total, avg, max)
3. Claps (total, avg, max)
4. Voters (total, avg, max)
"""

import json


def tag_frequency(data):
    tag_list = ["ethereum", "blockchain", "smart contract", "smart contracts", "solidity", "erc20",
                "web3", "security", "cryptocurrency", "metamask", "dapp", "dapps", "truffle",
                "tokens", "vyper", "ethereum blockchain",
                "bitcoin", "ico", "programming", "audit", "decentralization",
                ]

    for i in tag_list:
        count = 0
        for key in data:
            if i in [item.lower() for item in key['tags']]:
                count += 1
                # print(key['title'])
        print(i, "=", count)


def claps_voters_per_post(data):
    clap_list = []
    voter_list = []
    data_dict = dict()
    for key in data:
        clap_list.append(key['claps'])
        voter_list.append(key['voters'])
    for i, j in zip(clap_list, voter_list):
        data_dict[i] = j


def resp_clap_voter_1(data, tag):
    new_clap = []
    new_voter = []
    new_response = []
    for key in data:
        for i in key['tags']:
            if tag in i:
                new_clap.append(key['claps'])
                new_voter.append(key['voters'])
                new_response.append(key['responses'])

    # max_response = max(new_response)
    total_response = sum(new_response)
    avg_response = sum(new_response) / len(new_response)

    # max_clap = max(new_clap)
    total_clap = sum(new_clap)
    avg_clap = sum(new_clap) / len(new_clap)

    # max_voter = max(new_voter)
    total_voter = sum(new_voter)
    avg_voter = sum(new_voter) / len(new_voter)

    return total_response, round(avg_response, 2), total_clap, round(avg_clap, 2), \
           total_voter, round(avg_voter, 2)


def vulnerability_freq(data, word_list):
    vuln_count_list = []
    for i in word_list:
        count = 0
        for key in data:
            # do not use key['content'].lower() if search for "DoS"
            if i in key['content'].lower() or i in key['title'].lower() or i in key['tags']:
                count += 1
                # print(key['title'])
        vuln_count_list.append(count)
    return vuln_count_list


def security_tool_mention_freq(data, tool):
    count = 0
    for key in data:
        if tool in key['content'].lower() or i in key['title'].lower() or i in key['tags']:
            count += 1
            # print(key['title'])
    # print(tool, "=", count)
    return count

def co_occurrence_of_tools(tag):
    sec_tool_list = ["mythril", "mythx", "mythos", "oyente", "solhint", "solium", "ethlint",
                     "securify", "teether", "smartcheck", "manticore", "sonarsolidity", "ethir",
                     "maian", "solcheck", "solgraph", "solint", "vandal", "contractfuzzer",
                     "rattle", "sasc", "zeus", "contractlarva", "echinda", "ethertrust", "fsolidm",
                     "octopus", "osiris", "reguard", "scompile", "slither", "surya", "sūrya", "verisolid",
                     "verx", "vultron"]
    # sec_tool_list = ["sūrya"]
    for i in sec_tool_list:
        count = 0
        for key in post_data:
            if (i in key['content'].lower() or i in key['title'].lower() or i in key['tags']) \
                    and (("transaction ordering dependency" in key['content'].lower() or i in key['title'].lower()) \
                         or ("transaction-ordering dependency" in key['content'].lower() or i in key['title'].lower()) \
                         or ("transaction ordering dependent" in key['content'].lower() or i in key['title'].lower())):
                # or ("timestamp-depend" in key['content'].lower() or i in key['title'].lower())):
                count += 1
                # print(key['title'])
        print(i, "=", count)


if __name__ == '__main__':
    # Open the data file
    with open("related_data_rm_duplicacy.json", "r") as f:
        post_data = json.load(f)

    # Print tag frequencies
    print("Tag Frequencies:")
    print("-" * 40)
    tag_frequency(post_data)

    # Print response, clap, and voter counts
    print("\n\nResponse, Clap, and Voter Counts:")
    print("-" * 40)
    tags_list = ["Smart Contracts", "Smart Contract", "Solidity", "Web3", "Ethereum", "Truffle", "Security", "Metamask", "Remix",
                 "Ethereum Blockchain", "Blockchain", "Myetherwallet", "Erc20", "Token Sale",
                 "Cryptocurrency", "Bitcoin", "Ico", "ICO", "Programming", "Audit", "Decentralization", "Crypto"]
    for item in tags_list:
        a, b, c, d, e, f = resp_clap_voter_1(post_data, item)
        print(item, "-->", a, "&", b, "&", c, "&", d, "&", e, "&", f)

    # Print Vulnerability frequencies
    print("\n\nVulnerability Related Word Frequencies")
    print("-" * 40)
    vuln_word_list = ["security", "vulnerability", "vulnerab", "reentrancy", "re entrancy",
                 "re-entrancy", "race condition", "denial of service", "DoS", "transaction order",
                 "transactions order", "trasaction order depend", "transaction-ordering dependence",
                 "timestamp dependence", "integer overflow", "integer underflow"]
    vuln_freq_list = vulnerability_freq(post_data, vuln_word_list)
    sec_titles = ['vulnerability words', 'frequencies']
    table_data = [sec_titles] + list(zip(vuln_word_list, vuln_freq_list))

    for i, d in enumerate(table_data):
        line = '|'.join(str(x).ljust(30) for x in d)
        print(line)
        if i == 0:
            print('-' * len(line))

    # Print frequency of Security Tools
    print("\n\nSecurity Tools Mention Frequency:")
    print("-" * 40)
    sec_tool_list = ["mythril", "mythx", "mythos", "oyente", "solhint", "solium", "ethlint",
                     "securify", "teether", "smartcheck", "manticore", "sonarsolidity", "ethir",
                     "maian", "solcheck", "solgraph", "solint", "vandal", "contractfuzzer",
                     "rattle", "sasc", "zeus", "contractlarva", "echinda", "ethertrust", "fsolidm",
                     "octopus", "osiris", "reguard", "scompile", "slither", "surya", "sūrya", "verisolid",
                     "verx", "vultron", "checks-effects-interactions"]
    sec_tool_count_list = []
    for i in sec_tool_list:
        sec_tool_count_list.append(security_tool_mention_freq(post_data, i))

    sec_titles = ['security_tools', 'frequencies']
    table_data = [sec_titles] + list(zip(sec_tool_list, sec_tool_count_list))

    for i, d in enumerate(table_data):
        line = '|'.join(str(x).ljust(18) for x in d)
        print(line)
        if i == 0:
            print('-' * len(line))

    # titles = ['security_tools', 'frequencies']
    # data = [sec_tool_list] + list(zip(names, weights, costs, unit_costs))

    # for i, d in enumerate(data):
    #     line = '|'.join(str(x).ljust(12) for x in d)
    #     print(line)
    #     if i == 0:
    #         print('-' * len(line))

