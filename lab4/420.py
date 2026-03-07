import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    
    n_commands = int(input_data[0])
    
    g = 0  
    n = 0

    for i in range(1, n_commands * 2, 2):
        scope = input_data[i]
        value = int(input_data[i+1])
        
        if scope == "global":
            g += value
        elif scope == "nonlocal":
            n += value
            
    print(f"{g} {n}")

if __name__ == "__main__":
    solve()