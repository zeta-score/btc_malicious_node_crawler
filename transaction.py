from blockchain import blockexplorer
import pandas as pd
import blockchain




class n_hops:
    """
    Scraps all transactions of nodes which are n hops away from the starting list
    """
    def __init__(self, n, start):
        self.n = n
        self.start = start
        self.next = set(start)
        self.path = set(start)
        self.tx_map = dict()
        self.hop(n)
    def __set_next(self, next):
        self.next = next - next.intersection(self.path)
        self.path = self.path.union(self.next)

    def one_hop(self):
        next = set()
        for node in self.next:
            self.tx_map[node], _next = self.__traverse(node)
            next = next.union(_next)
        self.__set_next(next)

    def __traverse(self, address):
        try:
            node = blockexplorer.get_address(str(address))
            next = set([output.address for transaction in node.transactions for output in transaction.outputs])
            print('test')
            return node.transactions, next
        except blockchain.exceptions.APIException:
            return None,set()

    def hop(self,n):
        if n == 0:
            return
        else:
            self.one_hop()
            return self.hop(n-1)
if __name__ == "__main__":
    malicious_nodes_file = 'malicious_nodes.csv'
    malicious_nodes = pd.read_csv(malicious_nodes_file, sep=',')
    hop = n_hops(2, malicious_nodes['address'])
    print len(hop.tx_map.keys())
    print len(hop.next)
