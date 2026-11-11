import hashlib
import time
import json

class Block:
    def __init__(self, index, previous_hash, data, nonce=0):
        self.index = index
        self.timestamp = time.time()
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = self.calculate_hash()

    def calculate_hash(self):
        block_string = json.dumps(self.__dict__, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    # PoW 挖矿：找到前缀满足 difficulty 个 0 的 hash
    def mine_block(self, difficulty):
        while self.hash[:difficulty] != "0" * difficulty:
            self.nonce += 1
            self.hash = self.calculate_hash()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.difficulty = 4

    def create_block(self, data):
        if len(self.chain) == 0:
            previous_hash = "0"
            index = 0
        else:
            previous_block = self.chain[-1]
            previous_hash = previous_block.hash
            index = len(self.chain)
        block = Block(index, previous_hash, data)
        block.mine_block(self.difficulty)
        self.chain.append(block)
        self.save_block_to_file(block)
        return block

    def save_block_to_file(self, block):
        with open('blockchain.txt', 'a') as f:
            f.write(f"{block.index},{block.timestamp},{block.data},{block.hash},{block.previous_hash},{block.nonce}\n")

    def load_chain_from_file(self):
        """拓展实验1：从本地文件加载区块链"""
        self.chain = []
        try:
            with open("blockchain.txt", "r") as f:
                lines = f.readlines()
                for line in lines:
                    line = line.strip()
                    if not line:
                        continue
                    idx, ts, data, h, pre_h, nonce = line.split(",")
                    b = Block(int(idx), pre_h, data, int(nonce))
                    b.timestamp = float(ts)
                    b.hash = h
                    self.chain.append(b)
            print("成功从文件加载区块链！")
        except FileNotFoundError:
            print("文件不存在，新建一条链")
            self.create_block("Genesis Block")

    def print_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}, Timestamp: {block.timestamp}, Data: {block.data}, Hash: {block.hash}, Previous Hash: {block.previous_hash}, Nonce: {block.nonce}")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            prev_block = self.chain[i-1]
            if current_block.hash != current_block.calculate_hash():
                print(f"区块{i}哈希被篡改！")
                return False
            if current_block.previous_hash != prev_block.hash:
                print(f"区块{i}和前一区块链接断裂！")
                return False
            if current_block.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"区块{i}没有通过工作量证明！")
                return False
        print("整条区块链完整没有被篡改")
        return True


if __name__ == "__main__":
    bc = Blockchain()
    bc.load_chain_from_file()

    # 需要新增区块的时候，再取消下面两行注释
    # bc.create_block("First block data")
    # bc.create_block("Second block data")

    bc.print_chain()
    bc.is_chain_valid()

    # 模拟篡改测试，测试篡改时再取消注释
    # bc.chain[1].data = "I am hacked!!!"
