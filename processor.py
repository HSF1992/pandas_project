import pandas as pd

def 清洗数据(data,数值列=None):
    df = pd.DataFrame(data)
    if 数值列:
        for 列 in 数值列:
            df[列]=df[列].astype(str).str.replace(r"[^\d.]","",regex=True)
            df[列]=pd.to_numeric(df[列],errors="coerce")
        return df

def 导出Excel(df,文件名="输出.xlsx"):
    df.to_excel(文件名,index=False)
    return 文件名

def 画分布图(df,列名,文件名="分布图.png"):
    import matplotlib.pyplot as plt
    plt.rcParams["font.sans-serif"] = ["SimHei"]
    plt.rcParams["axes.unicode_minus"] = False

    df[列名].plot(kind="hist",bins=10,title=f"{列名}分布")
    plt.xlabel(列名)
    plt.ylabel("数量")
    plt.savefig(文件名)
    plt.close()
    return 文件名
