import kakuyomu_DL
print("DLしたいカクヨムのURLを入力してください")
url = input()
tmp = kakuyomu_DL.kakuyomu_DL(url)
tmp.save_text()