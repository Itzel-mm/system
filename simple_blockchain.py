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
        block_dict = {
            "index": self.index,
            "timestamp": self.timestamp,
            "data": self.data,
            "previous_hash": self.previous_hash,
            "nonce": self.nonce
        }
        block_string = json.dumps(block_dict, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

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
            print("【加载成功】从文件恢复区块链")
        except FileNotFoundError:
            print("【提示】文件不存在，新建链，生成创世区块")
            self.create_block("Genesis Block")

    def print_chain(self):
        for block in self.chain:
            print(f"Index:{block.index}, Data:{block.data}, Hash:{block.hash[:12]}...")

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            curr = self.chain[i]
            prev = self.chain[i-1]
            if curr.hash != curr.calculate_hash():
                print(f"校验失败：区块{i}哈希不匹配")
                return False
            if curr.previous_hash != prev.hash:
                print(f"校验失败：区块{i}与上一块断裂")
                return False
            if curr.hash[:self.difficulty] != "0" * self.difficulty:
                print(f"校验失败：区块{i}未通过PoW")
                return False
        print("校验通过，区块链合法")
        return True


if __name__ == "__main__":
    bc = Blockchain()
    bc.load_chain_from_file()

    # 测试3：仅从文件加载，不新增、不篡改

    bc.print_chain()
    bc.is_chain_valid()
