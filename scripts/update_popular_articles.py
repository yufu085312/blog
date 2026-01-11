import os
import sys
import json
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    DateRange,
    Dimension,
    Metric,
    RunReportRequest,
    OrderBy
)

def get_popular_articles():
    # 環境変数から設定を読み込む
    # JSON 鍵ファイルへのパス、または JSON そのものを環境変数に設定することを想定
    PROPERTY_ID = os.environ.get("GA4_PROPERTY_ID")
    # 認証情報の解決（google-cloud-analytics-data ライブラリは GOOGLE_APPLICATION_CREDENTIALS を自動参照する）
    
    if not PROPERTY_ID:
        print("Error: GA4_PROPERTY_ID is not set.")
        return

    client = BetaAnalyticsDataClient()

    request = RunReportRequest(
        property=f"properties/{PROPERTY_ID}",
        dimensions=[Dimension(name="pagePath")],
        metrics=[Metric(name="screenPageViews")],
        date_ranges=[DateRange(start_date="30daysAgo", end_date="today")],
        order_bys=[OrderBy(metric=OrderBy.MetricOrderBy(metric_name="screenPageViews"), desc=True)],
        limit=10 # 多めに取得して後でフィルタリング
    )

    response = client.run_report(request)

    popular_urls = []
    for row in response.rows:
        path = row.dimension_values[0].value
        # 不要なパスをフィルタリング（例：トップページ、タグ、カテゴリー一覧など）
        if path.startswith("/posts/") and not path == "/posts/":
            popular_urls.append(path)
            if len(popular_urls) >= 3: # TOP3まで
                break

    # Hugoのdataディレクトリに保存
    output_path = "data/popular_articles.json"
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(popular_urls, f, ensure_ascii=False, indent=2)
    
    print(f"Success: Updated {output_path} with {len(popular_urls)} articles.")

if __name__ == "__main__":
    get_popular_articles()
