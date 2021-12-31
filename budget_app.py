def truncate_word(l, s):
    return s if len(s) < l else s[:l]


class Category:
    def __init__(self, title):
        self.ledger = []
        self.title = truncate_word(30, title)

    def deposit(self, amount, desc=''):
        if amount:
            self.ledger.append(
                {"amount": amount, "description": desc}
            )

    def withdraw(self, amount, desc=''):
        if self.check_funds(amount):
            self.ledger.append(
                {"amount": -amount, "description": desc}
            )
            return True
        return False

    def get_balance(self):
        return sum(it['amount'] for it in self.ledger)

    def transfer(self, amount, cat):
        if self.withdraw(amount, f"Transfer to {cat.title}"):
            cat.deposit(amount, f"Transfer from {self.title}")
            return True
        return False

    def check_funds(self, amount):
        return amount <= self.get_balance()

    def __str__(self):
        l1 = self.title.center(30, "*")
        l2 = "\n".join(
            truncate_word(
                23,
                it["description"]).ljust(
                24,
                " ") +
            f'{it["amount"]:.2f}' for it in self.ledger)
        l3 = f"Total: {self.get_balance()}"
        return l1 + "\n" + l2 + "\n" + l3


def create_spend_chart(categories):
    dc = {}
    for cat in categories:
        dc[cat.title] = sum(it["amount"]
                            for it in cat.ledger if it["amount"] < 0)

    tot = -sum(val for val in dc.values())
    lst = []
    for key in dc.keys():
        lst.append((key, int(((dc[key] / tot) * 100) / 10) * 10))

    title = "Percentage spent by category"
    chart = [["100| "] + (["   "] * len(lst)),
             [" 90| "] + (["   "] * len(lst)),
             [" 80| "] + (["   "] * len(lst)),
             [" 70| "] + (["   "] * len(lst)),
             [" 60| "] + (["   "] * len(lst)),
             [" 50| "] + (["   "] * len(lst)),
             [" 40| "] + (["   "] * len(lst)),
             [" 30| "] + (["   "] * len(lst)),
             [" 20| "] + (["   "] * len(lst)),
             [" 10| "] + (["   "] * len(lst)),
             ["  0| "] + (["   "] * len(lst)),
             ["    -"] + (["---"] * len(lst)),
             ]

    for _ in range(max(len(it[0]) for it in lst)):
        chart += [
            ["     "] + (["   "] * len(lst))
        ]

    mapper = {a: b for a, b in zip(range(100, -10, -10), range(11))}

    for i, p in enumerate(lst):
        n = mapper[-p[1]]
        j = i + 1
        for row in range(n, 11):
            chart[row][j] = chart[row][j].replace(' ', 'o', 1)

        for row in range(12, len(chart)):
            if row - 12 < len(p[0]):
                chart[row][j] = p[0][row - 12] + chart[row][j][1:]

    return title + '\n' + '\n'.join(''.join(it) for it in chart)
