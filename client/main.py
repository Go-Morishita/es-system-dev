import requests
import webbrowser
import os

API_URL = "http://localhost:8000"


def main():
    gpt_req = {
        "instruction":
            """
            # Identity
            あなたは就職活動中の大学生のために、エントリーシート（ES）の設問に対する適切で説得力のある回答を日本語で作成するアシスタントです。

            # Instructions
            - 以下の情報を基に、各設問に対する文章を400字以上500文字以下で生成してください。
            - 改行文字は入れないでください。
            - 回答は自然で論理的な日本語にしてください。
            - 志望動機には企業の特徴と一致するような学生の強みを織り込んでください。
            - ガクチカでは成果・成長・学びを中心にまとめてください。
            - 出力形式は以下に示すXMLフォーマットで返答してください。

            # Output format
            <es_answers>
            <name>（氏名）</name>
            <question_answers>
                <item>
                    <question>（設問の内容）</question>
                    <answer>（設問の回答）</answer>
                </item>
                ...
            </question_answers>
            </es_answers>
            """,
        "user_input":
            """
            企業名：日立製作所
            設問①：日立製作所を志望する理由は何ですか？
            設問②：学生の時に特に力を入れたことは何ですか？
            設問③：あなたの強みは何ですか？
            設問④：あなたの弱みは何ですか？
            氏名：森下 剛
            大学・学部・学科：青山学院大学・理工学部・情報テクノロジー学科
            GPA：3.6
            ガクチカ：
            - 体育会水泳部（水泳歴20年）
            - 個人開発でWebに強い知見がある（ハッカソンなどでの入賞経験あり）
            - 大学4年次にCG研究で国際学会での発表経験あり
            """
    }

    # /get_json を呼び出して JSON を取得
    res = requests.post(f"{API_URL}/get_json", json=gpt_req)
    res.raise_for_status()
    config = res.json()

    # /create_pdf を呼び出して PDF バイナリを取得
    res_pdf = requests.post(f"{API_URL}/create_pdf", json=config)
    res_pdf.raise_for_status()

    # ファイルに保存してブラウザで開く
    output_path = "output.pdf"
    with open(output_path, "wb") as f:
        f.write(res_pdf.content)

    # Windows / macOS / Linux 共通で開けるように
    webbrowser.open(f"file://{os.path.abspath(output_path)}")

    print("取得したJSON:")
    print(config)


if __name__ == "__main__":
    main()
