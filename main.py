import random
from decimal import Decimal, ROUND_HALF_UP

# 生成六條路線, 前兩條的起點不能相同
def gen_paths():
  paths = [[i] for i in [*random.sample(range(7), 2), *random.choices(range(7), k=4)]]
  for path in paths:
    while len(path) < 15:
      path.append(find_next(paths, len(path), path[-1]))
  return paths  
  
def find_next(paths, floor, curr):
  next = [curr] # 可能的下個節點
  if curr > 0:
    # 檢驗向左是否會產生交叉路徑
    cross = False
    for path in paths:
      if len(path) == floor:
        break
      if path[floor - 1] == curr - 1 and path[floor] == curr:
        cross = True
        break
    if not cross:
      next.append(curr - 1)
  if curr < 6:
    # 檢驗向右是否會產生交叉路徑
    cross = False
    for path in paths:
      if len(path) == floor:
        break
      if path[floor - 1] == curr + 1 and path[floor] == curr:
        cross = True
        break
    if not cross:
      next.append(curr + 1)
  return random.choice(next)

def init_sls_map(paths):
  # 整個地圖為 7 * 16 (寬 * 高) 的網格, 第 16 層固定為 Boss
  sls_map = [[{"type": None, "next": [], "prev": [], "path": ""} for x in range(7)] for y in range(15)]
  for path in paths:
    for floor in range(15):
      if floor == 0:
        sls_map[floor][path[floor]]["type"] = "M" # 第 1 層固定為普通怪
      elif floor == 8:
        sls_map[floor][path[floor]]["type"] = "T" # 第 9 層固定為寶箱
      elif floor == 14:
        sls_map[floor][path[floor]]["type"] = "R" # 第 15 層固定為營火
      else:
        sls_map[floor][path[floor]]["type"] = "*" # 剩餘的房間類型待定
      if floor < 14:
        sls_map[floor][path[floor]]["next"].append(path[floor + 1])
      if floor > 0:
        sls_map[floor][path[floor]]["prev"].append(path[floor - 1])

  # 如果兩個初始節點在第二層就相遇了, 刪除其中一條邊避免路徑重複
  for pos in range(7):
    for p in sls_map[1][pos]["prev"][1:]:
      sls_map[0][p]["next"].remove(pos)
      if not len(sls_map[0][p]["next"]):
        sls_map[0][p]["type"] = None
  # 將 next 可視化
  for floor in range(14):
    for pos in range(7):
      next = sls_map[floor][pos]["next"]
      left  = "\\" if pos - 1 in next else " "
      mid   = "|" if pos in next else " "
      right = "/" if pos + 1 in next else " "
      sls_map[floor][pos]["path"] = left + mid + right
  return sls_map

def gen_room_pool(sls_map):
  # 將待定房間數根據不同房間類型乘上一定比例生成類型池
  count = sum(node["type"] == "*" for x in sls_map for node in x)
  PROB = {
    "ELITE": 0.128, # 0.08 * 1.6
    "EVENT": 0.22,
    "SHOP": 0.05,
    "REST": 0.12
  }
  pool = []
  pool.extend(["E"] * round_half_up(PROB["ELITE"] * count))
  pool.extend(["?"] * round_half_up(PROB["EVENT"] * count))
  pool.extend(["S"] * round_half_up(PROB["SHOP"] * count))
  pool.extend(["R"] * round_half_up(PROB["REST"] * count))
  pool.extend(["M"] * (count - len(pool))) # 剩餘的房間用普通怪填充
  return pool

def set_room(sls_map, pool):
  for floor in range(1, 14):
    for pos in range(7):
      room = sls_map[floor][pos]
      if not room["type"] == "*":
        continue
      random.shuffle(pool) # 打亂類型池
      # 開始遍歷直到滿足條件的房間類型被選到
      for i, room_type in enumerate(pool):
        # 不能連續兩個菁英怪、商人、營火
        if room_type in ["E", "S", "R"] and room_type in (sls_map[floor - 1][x]["type"] for x in room["prev"]):
          continue
        # 菁英怪與營火只會在大於等於 6 層出現
        if room_type in ["E", "R"] and floor < 5:
          continue
        siblings = []
        for p in room["prev"]:
          siblings.extend([sls_map[floor][x]["type"] for x in sls_map[floor - 1][p]["next"]])
        # 兩個房間如果有同個父節點, 則它們的類型不能相同
        if room_type in siblings:
          continue
        # 第 14 層不能是營火 (因為第 15 層一定是營火)
        if room_type == "R" and floor == 13:
          continue
        room["type"] = room_type
        pool.pop(i)
        break
  # 將沒有合適類型的房間指定為普通怪
  for floor in range(1, 14):
    for pos in range(7):
      room = sls_map[floor][pos]
      if room["type"] == "*":
        room["type"] = "M"

# 處理四捨五入
def round_half_up(x, ndigits=0):
  q = Decimal('1').scaleb(-ndigits)      # 10**(-ndigits)
  d = Decimal(str(x)).quantize(q, rounding=ROUND_HALF_UP)
  return float(d) if ndigits else int(d)

# 樓層由下到上畫出房間與路徑
def show():
  for x in range(15):
    floor = 14 - x
    print(f"   ", end="")
    for pos in range(7):
      if floor < 14:
        if sls_map[floor][pos]["type"]:
          print(sls_map[floor][pos]["path"], end="")
        else:
          print("   ", end="")
    print()
    print(f"{(floor + 1):02} ", end="")
    for pos in range(7):
      if sls_map[floor][pos]["type"]:
        print(f" {sls_map[floor][pos]["type"]} ", end="")
      else:
        print(f"   ", end="")
    print()

if __name__ == "__main__":
  paths = gen_paths()
  sls_map = init_sls_map(paths)
  pool = gen_room_pool(sls_map)
  set_room(sls_map, pool)
  show()
