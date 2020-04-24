#!/usr/bin/env python
# -*- coding: utf8 -*-

import eel
import sys
import oa_core as core
import random
import subprocess
import webbrowser
import os
import datetime
import re
from threading import Timer
import urllib.request
import urllib.parse
import html
import otfdlib


@eel.expose
def change_theme(_css_theme_path):
    _css_file_path = "resource/css/layout.css"
    _old_css = ""
    with open(_css_file_path, mode="r") as _css_file:
        _old_css = _css_file.read()
    if os.path.exists(f"resource/css/{_css_theme_path}") is False:
        _light_theme = ""
        with open("resource/css/theme/light_theme.css", mode="r") as _light_theme_file:
            _light_theme = _light_theme_file.read()
        with open(f"resource/css/{_css_theme_path}", mode="w") as _new_theme:
            _new_theme.write(_light_theme)
    _new_css = f'@import url("{_css_theme_path}");{_old_css[_old_css.find(";") + 1:]}'
    with open(_css_file_path, mode="w") as _css_file:
        _css_file.write(_new_css)
    write_setting("theme", _css_theme_path)
    return


@eel.expose
def write_custom_css_theme(_value):
    if len(_value) == 5:
        _custom_css_data = ":root {\n    --bg: " + _value[0] + ";\n    --card_bg: " + _value[1] + ";\n    --text: " + _value[2] + ";\n    --shadow: " + _value[3] + ";\n    --theme_color: " + _value[4] + ";\n}"
        with open("resource/css/theme/custom_theme.css", mode="w") as _f:
            _f.write(_custom_css_data)
        return
    else:
        core.showerror("カスタムCSSテーマに不正な値を書き込もうとしています。")
        return


@eel.expose
def check_current_css_theme_information():
    css_file_path = read_setting("theme")
    with open(f"resource/css/{css_file_path}", mode="r", encoding="utf-8_sig") as f:
        css = f.read()
        pattern = re.compile(":root \{.*?\}", re.MULTILINE | re.DOTALL)
        value = re.sub("(:root \{)|\}|( *)|-|;", "", re.search(pattern, css).group())
        root = otfdlib.Otfd()
        root.load_from_string(value)
        root.parse()
        return root.get_value_list()


@eel.expose
def read_setting(_setting_name):
    return core.read_setting("resource/setting/setting.otfd", _setting_name)


@eel.expose
def write_setting(_setting_name, _setting_value):
    return core.write_setting("resource/setting/setting.otfd", _setting_name, _setting_value)


@eel.expose
def read_flag(_flag_name):
    return core.read_flag("resource/setting/flag.otfd", _flag_name)


@eel.expose
def set_flag(_flag_name, _flag_value):
    core.set_flag("resource/setting/flag.otfd", _flag_name, _flag_value)
    return


@eel.expose
def make_response(_not_normalized_query):
    _not_normalized_query = _not_normalized_query.replace("\n", "").replace("\r", "")
    _query = core.normalize(_not_normalized_query)
    if core.judge(_query, ["じゃんけん", "ジャンケン"]):
        hand_shapes = ["グー", "チョキ", "パー"]
        selected_hand_shape = hand_shapes[random.randint(0, 2)]
        return [f"ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私は{selected_hand_shape}です。", f"ジャンケンですか。良いですね。やりましょう。それではいきますよ。ジャン　ケン　ポン。私は{selected_hand_shape}です。"]
    elif core.judge(_query, ["イースターエッグ", "ゲーム", "宇宙船", "宇宙戦艦", "spacebattleship", "game", "easteregg"]):
        subprocess.Popen(["python", "resource/python/easter_egg.py"])
        return ["イースターエッグを起動します。", "イースターエッグを起動します。"]
    elif core.judge(_query, [".*の(面積|めんせき|広さ|ひろさ|大きさ|おおきさ)"]):
        area_value = core.respond(core.load_dictionary("resource/dictionary/country_information_dictionary/area_dictionary.otfd"), _query)
        if area_value[0] == "そうですか。":
            webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), _not_normalized_query))
            return ["面積を検索します。", "面積を検索します。"]
        else:
            return [f"{area_value[2]}の面積は{area_value[0]}です。", f"{area_value[2]}の面積は{area_value[1]}です。"]
    elif core.judge(_query, [".*(の|にある)(首都|しゅと)"]):
        capital_name = core.respond(core.load_dictionary("resource/dictionary/country_information_dictionary/capital_dictionary.otfd"), _query)
        if capital_name[0] == "そうですか。":
            webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), _not_normalized_query))
            return ["首都を検索します。", "首都を検索します。"]
        else:
            return [f"{capital_name[2]}の首都は{capital_name[0]}です。", f"{capital_name[2]}の首都は{capital_name[1]}です。"]
    elif core.judge(_query, [".*(の|使.*?いる)(言語|げんご|言葉|ことば|コトバ|公用語|こうようご)"]):
        language = core.respond(core.load_dictionary("resource/dictionary/country_information_dictionary/language_dictionary.otfd"), _query)
        if language[0] == "そうですか。":
            webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), _not_normalized_query))
            return ["言語を検索します。", "言語を検索します。"]
        else:
            return [f"{language[2]}の言語は{language[0]}です。", f"{language[2]}の言語は{language[1]}です。"]
    elif core.judge(_query, [".*(の|に.*?(いる|でる))(人口|人口|(人|ひと)(の|)(数|かず))"]):
        population = core.respond(core.load_dictionary("resource/dictionary/country_information_dictionary/population_dictionary.otfd"), _query)
        if population[0] == "そうですか。":
            webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), _not_normalized_query))
            return ["人口を検索します。", "人口を検索します。"]
        else:
            return [f"{population[2]}の人口は{population[0]}です。", f"{population[2]}の人口は{population[1]}です。"]
    elif core.judge(_query, [".*(の|で)(宗教|しゅうきょう|信仰|しんこう|国教|こっきょう)"]):
        religion = core.respond(core.load_dictionary("resource/dictionary/country_information_dictionary/religion_dictionary.otfd"), _query)
        if religion[0] == "そうですか。":
            webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), _not_normalized_query))
            return ["宗教を検索します。", "宗教を検索します。"]
        else:
            return [f"{religion[2]}の宗教は{religion[0]}です。", f"{religion[2]}の宗教は{religion[1]}です。"]
    elif core.judge(_query, ["予定", "よてい", "カレンダ", "かれんだ", "calender", "リマインダ", "リマインド", "りまいんだ", "りまいんど", "remind"]):
        webbrowser.open_new("https://calendar.google.com/")
        return ["Googleカレンダーを開きます", "Googleカレンダーを開きます。"]
    elif core.judge(_query, ["マップ", "まっぷ", "地図", "ちず", "場所", "ばしょ", "どこ", "何処", "行き方", "いきかた", "ゆきかた", "行きかた", "いき方", "ゆき方", "案内", "あんない", "道"]):
        webbrowser.open_new("https://google.com/maps/search/" + urllib.parse.quote(_not_normalized_query))
        return [f"Googleマップで「{_query}」を検索します。", f"Googleマップで「{_query}」を検索します。"]
    elif core.judge(_query, ["ストップウォッチ", "ストップウオッチ", "stopwatch"]):
        webbrowser.open_new("https://google.com/search?q=stopwatch&hl=en")
        return ["ストップウォッチを表示します。", "ストップウォッチを表示します。"]
    elif core.judge(_query, ["計算", "けいさん", "電卓", "でんたく"]):
        webbrowser.open_new(core.generate_search_engine_url("google", "電卓"))
        return ["電卓を開きます。", "電卓を開きます。"]
    elif core.judge(_query, ["何時", "時間", "時刻", "時計", "なんじ", "じかん", "じこく", "とけい", "日付", "ひづけ", "何日", "なんにち", "日にち", "ひにち"]):
        time = datetime.datetime.now()
        time = time.strftime('%Y年%m月%d日 %H:%M:%S')
        return [f"現在は{time}です。", f"現在は{time}です。"]
    elif core.judge(_query, ["twitter", "ツイッタ", "ついった", "tweet", "ツイート", "ついーと"]):
        webbrowser.open_new("https://twitter.com/")
        return ["Twitterを開きます。", "Twitterを開きます。"]
    elif core.judge(_query, ["コロナ", "ころな", "corona", "covid19", "sarscov2", "感染", "かんせん", "肺炎", "はいえん"]):
        webbrowser.open_new("https://corona.go.jp/")
        return ["内閣官房の新型コロナウイルスに関するページを表示します。", "内閣官房の新型コロナウイルスに関するページを表示します。"]
    elif core.judge(_query, ["facebook", "フェイスブック", "ふぇいすぶっく", "フェースブック", "ふぇーすぶっく"]):
        webbrowser.open_new("https://www.facebook.com/")
        return ["Facebookを開きます。", "Facebookを開きます。"]
    elif core.judge(_query, ["テレビ", "tv", "てれび", "番組", "ばんぐみ", "tver", "ティーバ", "てぃーば"]):
        webbrowser.open_new("https://tver.jp/")
        return ["TVerを開きます。", "TVerを開きます。"]
    elif core.judge(_query, ["youtube", "ユーチューブ", "ゆーちゅーぶ", "ようつべ", "ヨウツベ", "よーぶべ", "ヨーツベ"]) and core.judge(_query, ["て何" ,"てなに", "意味", "とは", "教え", "おしえ", "検索", "けんさく", "調べ", "しらべ", "調査", "ちょうさ", "再生", "さいせい", "見せ", "観せ", "みせ", "見たい", "観たい", "みたい"]):
        webbrowser.open_new(core.generate_search_engine_url("https://www.youtube.com/results?search_query=", _not_normalized_query, True))
        return [f"YouTubeで「{_not_normalized_query}」を検索します。", f"YouTubeで「{_not_normalized_query}」を検索します。"]
    elif core.judge(_query, ["youtube", "ユーチューブ", "ゆーちゅーぶ", "ようつべ", "ヨウツベ", "よーぶべ", "ヨーツベ"]):
        webbrowser.open_new("https://www.youtube.com/")
        return ["YouTubeを開きます。", "YouTubeを開きます。"]
    elif core.judge(_query, ["instagram", "インスタ", "いんすた"]):
        webbrowser.open_new("https://www.instagram.com/")
        return ["Instagramを開きます。", "Instagramを開きます。"]
    elif core.judge(_query, ["github", "ギットハブ", "ぎっとはぶ"]):
        webbrowser.open_new("https://github.com/")
        return ["GitHubを開きます。", "GitHubを開きます。"]
    elif core.judge(_query, ["地震", "じしん"]):
        webbrowser.open_new("https://www.jma.go.jp/jp/quake/")
        return ["気象庁の地震情報のページを開きます。", "気象庁の地震情報のページを開きます。"]
    elif core.judge(_query, ["トレンド", "とれんど", "trend"]):
        webbrowser.open_new("https://trends.google.com/trends/trendingsearches/daily?geo=JP")
        return ["Googleトレンドを開きます。", "Googleトレンドを開きます。"]
    elif core.judge(_query, ["news", "ニュース", "にゅーす"]):
        webbrowser.open_new(read_setting("news_site_url"))
        return ["ニュースを開きます。", "ニュースを開きます。"]
    elif core.judge(_query, ["翻訳", "ほんやく"]):
        webbrowser.open_new("https://translate.google.co.jp/?hl=ja")
        return ["Google翻訳を開きます。", "Google翻訳を開きます。"]
    elif core.judge(_query, ["メール", "めーる", "mail"]):
        webbrowser.open_new("https://mail.google.com/")
        return ["Gmailを開きます。", "Gmailを開きます。"]
    elif core.judge(_query, ["ラジオ", "らじお", "radio"]):
        webbrowser.open_new("http://radiko.jp/")
        return ["radikoを開きます。", "radikoを開きます。"]
    elif core.judge(_query, ["写真", "しゃしん", "画像", "がぞう", "フォト", "ふぉと", "photo", "ピクチャ", "ぴくちゃ", "picture"]):
        webbrowser.open_new("https://photos.google.com/")
        return ["Googleフォトを開きます。", "Googleフォトを開きます。"]
    elif core.judge(_query, ["メモ", "memo", "めも", "記憶", "きおく", "記録", "きろく"]) and core.judge(_query, ["削除", "さくじょ", "消去", "しょうきょ", "クリア", "clear", "くりあ", "消し", "けし", "忘れ", "わすれ", "破棄", "はき", "放棄", "ほうき"]):
        if os.path.exists("memo.txt") is False:
            return ["覚えているメモはありません。", "覚えているメモはありません。"]
        else:
            _memo = ""
            with open("memo.txt", mode="r", newline="") as _f:
                _memo = _f.read()
            if _memo.strip() == "":
                return ["覚えているメモはありません。", "覚えているメモはありません。"]
            else:
                if core.judge(_query, ["\d+?((つ|個|こ|コ|番|ばん)(|め|目))"]):
                    _splited_memo = _memo.splitlines()
                    _memo_index = int(re.search("\d+?", (re.search("\d+?((つ|個|こ|コ|番|ばん)(|め|目))", _query).group())).group())
                    if _memo_index > len(_splited_memo):
                        return ["削除するメモの番号が正しくありません。", "削除するメモの番号が正しくありません。"]
                    else:
                        _splited_memo.pop(_memo_index - 1)
                        with open("memo.txt", mode="w", newline="") as _f:
                            _f.write("\n".join(_splited_memo))
                        return [f"{_memo_index}つ目のメモを削除しました。", f"{_memo_index}つ目のメモを削除しました。"]
                with open("memo.txt", mode="w", newline="") as _f:
                    _f.write("")
                return ["覚えているメモをすべて消去しました。", "覚えているメモをすべて消去しました。"]
    elif core.judge(_query, ["メモ", "memo", "めも", "何", "なに", "内容", "ないよう"]) and core.judge(_query, ["覚えている", "おぼえている", "覚えてる", "おぼえてる", "記憶", "きおく", "記録", "きろく", "教え", "おしえ", "読", "よめ", "よん", "よみ"]):
        if os.path.exists("memo.txt") is False:
            return ["覚えているメモはありません。", "覚えているメモはありません。"]
        else:
            _memo = ""
            with open("memo.txt", mode="r", newline="") as _f:
                _memo = _f.read()
            if _memo.strip() == "":
                return ["覚えているメモはありません。", "覚えているメモはありません。"]
            else:
                _memo_list = _memo.strip().split("\n")
                _memo_list = [f"{num + 1}つ目は、「{_memo_list[num]}」です。" for num in range(len(_memo_list))]
                _memo_content_to_read = "".join(_memo_list)
                return [f"覚えているメモを読み上げます。{_memo_content_to_read}以上が、覚えているメモです。", f"覚えているメモを読み上げます。{_memo_content_to_read}以上が、覚えているメモです。"]
    elif core.judge(_query, ["メモ", "memo", "めも", "覚えて", "おぼえて", "覚えと", "おぼえと", "記憶", "きおく", "記録", "きろく"]):
        if os.path.exists("memo.txt") is False:
            with open("memo.txt", mode="w", newline="") as _f:
                pass
        _memo_content = re.sub("(と(|いう(|ように|ふうに|風に))|(|っ)て(|いう(|ように|ふうに|風に)))(メモ|memo|めも|記憶|きおく|記録|きろく|)(覚え(てお|と|て)(いて|け|ろ|ください|下さい)|し(て(|下さい|ください)|てお(け|きなさい|いて(|ください|下さい))|と(け|いて(|ください|下さい))|ろ|)|)$", "", _not_normalized_query)
        with open("memo.txt", mode="a", newline="") as _f:
            _f.write(f"{_memo_content}\n")
        if _memo_content == "":
            return ["申し訳ありません。処理に失敗しました。別の言い方をお試し下さい。", "申し訳ありません。処理に失敗しました。別の言い方をお試し下さい。"]
        else:
            return [f"「{_memo_content}」とメモしました。", f"「{_memo_content}」とメモしました。"]
    elif core.judge(_query, ["て何" ,"てなに", "意味", "とは", "教え", "おしえ", "検索", "けんさく", "調べ", "しらべ", "調査", "ちょうさ"]):
        search_engine = read_setting("search_engine")
        webbrowser.open_new(core.generate_search_engine_url(read_setting("search_engine"), _not_normalized_query))
        return [f"{search_engine}で「{_not_normalized_query}」を検索します。", f"{search_engine}で「{_not_normalized_query}」を検索します。"]
    elif core.judge(_query, ["サイコロ", "さいころ", "ダイス", "だいす", "dice"]):
        max_number = 6
        if core.judge(_query, ["\d(面|めん)"]):
            max_number = re.sub("(面|めん)", "", re.search("\d*(面|めん)", _query).group())
        if int(max_number) <= 0:
            max_number = 6
        dice_result = random.randint(1, int(max_number))
        max_number_message = ""
        if max_number != 6:
            max_number_message = f"{max_number}面"
        return [f"{max_number_message}サイコロを振りますね。{dice_result}が出ました。", f"{max_number_message}サイコロを振りますね。{dice_result}が出ました。"]
    elif core.judge(_query, ["コイン", "こいん", "coin"]) and core.judge(_query, ["トス", "とす", "toss", "投げ", "なげ"]):
        coin = ["表", "裏"]
        result = coin[random.randint(0, 1)]
        return [f"コイントスをしますね。{result}が出ました。", f"コイントスをしますね。{result}が出ました。"]
    elif core.judge(_query, ["みくじ", "御籤", "神籤", "ミクジ"]):
        fortune_repertoire = ["大吉", "吉", "中吉", "小吉", "末吉", "凶", "大凶"]
        result = fortune_repertoire[random.randint(0, len(fortune_repertoire) - 1)]
        return [f"おみくじをします。ガラガラ...。結果は・・・{result}です。", f"おみくじをします。ガラガラ...。結果は・・・{result}です。"]
    elif core.judge(_query, ["さようなら", "サヨウナラ", "さよなら", "サヨナラ", "バイバイ", "終了", "しゅうりょう", "シャットダウン", "しゃっとだうん", "shutdown", "下がりなさい", "下がれ", "さがりなさい", "さがれ", "邪魔", "じゃま", "消え", "きえ", "失せ", "うせ", "またね", "また会おう", "またあおう", "また今度", "またこんど"]) and read_flag("exit_by_voice_command"):
        return ["", "<script>window.close()</script>"]
    elif core.judge(_query, ["タイマ", "たいま", "砂時計", "すなどけい", "すなとけい"]) and core.judge(_query, ["設定", "せってい", "セット", "鳴ら", "なら", "かけ"]):
        time = set_intelligent_timer(_query)
        return [f"{time}後にタイマーを設定しました。アプリを閉じるとタイマーは破棄されます。", f"{time}後にタイマーを設定しました。アプリを閉じるとタイマーは破棄されます。"]
    else:
        _response = core.respond(dictionary, _query)
        _user_name = read_setting("user_name")
        return [_response[0].format(user_name=_user_name), _response[1].format(user_name=_user_name)]


def set_intelligent_timer(_query):
    hours = 0
    minutes = 0
    seconds = 0
    _query = re.sub(r"じかん|ジカン|hour", "時間", _query)
    _query = re.sub(r"ふん|フン|ぷん|プン|minute", "分", _query)
    _query = re.sub(r"びょう|ビョウ|second", "秒", _query)
    _query = _query.replace("半", "30")
    if '時間' in _query:
        hours = int(re.search(r'\d*', re.search(r'\d*時間', _query).group()).group())
    if '分' in _query:
        minutes = int(re.search(r'\d*', re.search(r'\d*分', _query).group()).group())
    if '秒' in _query:
        seconds = int(re.search(r'\d*', re.search(r'\d*秒', _query).group()).group())
    time = ""
    if hours:
        time = f"{hours}時間"
    if minutes:
        time += f"{minutes}分"
    if seconds:
        time += f"{seconds}秒"
    if not time:
        time = "0秒"
    td = datetime.timedelta(hours=hours, minutes=minutes, seconds=seconds)
    total_seconds = td.total_seconds()
    timer = Timer(total_seconds, core.showinfo, (f'{time}経ちました！',))
    timer.start()
    return time


@eel.expose
def check_update():
    return core.check_update("resource/information.txt",
                             "https://raw.githubusercontent.com/Robot-Inventor/ORIZIN-Agent-HTML/master/resource/information.txt",
                             "https://raw.githubusercontent.com/Robot-Inventor/ORIZIN-Agent-HTML/master/update_message.txt")


def get_wiki_data(keyword):
    keyword = urllib.parse.quote(keyword)
    url = f'https://ja.wikipedia.org/w/api.php?format=xml&action=query&prop=revisions&titles={keyword}&rvprop=content&rvparse'
    data = urllib.request.urlopen(url).read().decode('utf-8')
    data = html.unescape(re.sub('[\n\r]', '', data))
    return data


def search_wiki(keyword):
    data = get_wiki_data(keyword)
    if 'redirectText' in data:
        data = get_wiki_data(re.sub('<.*?>', '', re.search('<a href.*?>.*?</a>', data).group()))
    data = re.sub('<.*?>', '', re.search(r'<p>.*?</p>', data).group())
    return re.sub('\[\d\]', '', html.unescape(data))


if __name__ == "__main__":
    try:
        dictionary = core.load_dictionary("resource/dictionary/dictionary.otfd")
    except Exception as error_message:
        core.showerror(error_message)
        sys.exit()
    if os.path.exists("resource/setting/setting.otfd") is False:
        change_theme("theme/light_theme.css")
    core.solve_setting_conflict("resource/setting/default_setting.otfd", "resource/setting/setting.otfd")
    core.solve_setting_conflict("resource/setting/default_flag.otfd", "resource/setting/flag.otfd")
    eel.init("resource")
    if read_setting("setup_finished") == "False":
        eel.start("/html/setup.html")
    else:
        eel.start("/html/splash.html")
