# AnsibleでMacを管理
Mac Book Proを衝動買いしてしまいました。
サーバー類は全てAnsibleで管理しているのでMacもAnsibleで構築・運用していきたいと思います。
今はMacのセットアップにAnsibleを使うというのも一般的みたいですね。

# はじめに
ちなみに衝動買いしたMacのスペックはざっと以下のような感じです。

* Mac Book Pro (2.3GHzクアッドコアIntel Core i5 Retina)
* macOS High Sierra 10.13 / メモリ 16GB

## Homebrewのインストール
[公式サイト](https://brew.sh/)にもありますが、以下のコマンドを実行します。
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

続いてAnsibleをインストールします。Terminalを開いて下記コマンドを実行していきます。
```
brew install ansible
<!--mkdir /etc/ansible-->
<!--curl -L https://raw.githubusercontent.com/toshi-click/dev.test/master/provision/mac/ansible.cfg -o /etc/ansible/ansible.cfg-->
```

## Ansible Playbookをシェルから実行する
```
cd ~~~~~ここまで
sudo ansible-playbook -l local -i inventory/default.yml playbooks/my-mac.yml
```

# gitkeyの登録
```
cp ~/git/key/git_key/rsa_4096 ~/.ssh/rsa_4096
chmod 600 ~/.ssh/rsa_4096
```
