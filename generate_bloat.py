def generate_bloat(file_name, lines=1000000):
    with open(file_name, 'w') as f:
        for i in range(lines):
            f.write(f"// This is bloat line {i}\n")

if __name__ == "__main__":
    generate_bloat("bloat_file.txt")
