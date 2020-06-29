def delete_all(s, what):
    try:
        t = s.split(what)
        s_new = "".join(t)
        return s_new
    except:
        raise Exception("there is an error")


if __name__ == "__main__":
    # print(delete_all("mamapolodogpolopok_er", "polo"))
    print(delete_all("mamapolodogpolopok_er", 1))

