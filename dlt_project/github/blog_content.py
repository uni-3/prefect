from prefect_github import GitHubCredentials
import base64
from dataclasses import dataclass
import requests
import dlt
from typing import List,  Optional

owner = "uni-3"
repo = "gatsby-blog"


@dataclass
class MarkdownFile:
    name: str
    path: str
    content: str


class GitHubMarkdownFetcher:
    def __init__(self, owner: str, repo: str, path: Optional[str] = "", token: Optional[str] = None):
        """
        GitHubのMarkdownファイルを取得するためのクラス

        Args:
            owner: GitHubのユーザー名またはオーガニゼーション名
            repo: リポジトリ名
            path: 精査するパス
            token: GitHubのパーソナルアクセストークン（オプション）
        """
        self.owner = owner
        self.repo = repo
        self.path = path
        self.base_url = "https://api.github.com"
        self.headers = {
            "Accept": "application/vnd.github.v3+json"
        }
        if token:
            self.headers["Authorization"] = f"Bearer {token}"

    def get_all_files(self) -> List[MarkdownFile]:
        """
        指定されたパス以下の全Markdownファイルを一度に取得

        Args:
            path: 取得を開始するパス（デフォルトはリポジトリのルート）

        Returns:
            MarkdownFileオブジェクトのリスト
        """
        try:
            url = f"{self.base_url}/repos/{self.owner}/{self.repo}/git/trees/main"
            # recursive=1 を追加してすべてのファイルを一度に取得
            params = {"recursive": "1"}

            response = requests.get(url, headers=self.headers, params=params)
            response.raise_for_status()

            tree = response.json()["tree"]
            files = []

            # pathが指定されている場合は、そのパス以下のファイルのみをフィルタ
            for item in tree:
                if (item["type"] == "blob" and
                    item["path"].endswith(".md") and
                        item["path"].startswith(self.path)):

                    content = self._get_file_content(item["path"])
                    files.append(MarkdownFile(
                        name=item["path"].split("/")[-1],
                        path=item["path"],
                        content=content
                    ))

            return files

        except requests.exceptions.RequestException as e:
            print(f"Error fetching files: {e}")
            raise

    def _get_file_content(self, file_path: str) -> str:
        """
        ファイルの内容を取得

        Args:
            file_path: ファイルのパス

        Returns:
            ファイルの内容（文字列）
        """
        url = f"{self.base_url}/repos/{self.owner}/{self.repo}/contents/{file_path}"
        response = requests.get(url, headers=self.headers)
        response.raise_for_status()

        content = response.json()
        if content.get("encoding") == "base64":
            return base64.b64decode(content["content"]).decode('utf-8')
        else:
            response = requests.get(
                content["download_url"], headers=self.headers)
            response.raise_for_status()
            return response.text


@dlt.resource()
def get_resources(fetcher: GitHubMarkdownFetcher):
    markdown_files = fetcher.get_all_files()
    content = [{"path": m.path, "text": m.content} for m in markdown_files]
    yield content


def main():
    dlt.secrets["sources.rest_api_pipeline.github_source"] = GitHubCredentials.load(
        "github-credentials-block").token.get_secret_value()
    fetcher = GitHubMarkdownFetcher(
        owner=owner,
        repo=repo,
        path="content",
        token=dlt.secrets["sources.rest_api_pipeline.github_source"]
    )

    try:
        print(get_resources(fetcher))

    except Exception as e:
        print(f"エラーが発生しました: {e}")


if __name__ == "__main__":
    main()
