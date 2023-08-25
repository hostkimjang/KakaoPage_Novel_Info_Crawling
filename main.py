import time
import requests
from sort_data import sort_data
from store import store_info
from bs4 import BeautifulSoup as bs
import json
import pprint

url = 'https://page.kakao.com/graphql/'

headers = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36"
}

query = """
    query staticLandingGenreSection($sectionId: ID!, $param: StaticLandingGenreParamInput!) {
  staticLandingGenreSection(sectionId: $sectionId, param: $param) {
    ...Section
  }
}
    
    fragment Section on Section {
  id
  uid
  type
  title
  ... on DependOnLoggedInSection {
    loggedInTitle
    loggedInScheme
  }
  ... on SchemeSection {
    scheme
  }
  ... on MetaInfoTypeSection {
    metaInfoType
  }
  ... on TabSection {
    sectionMainTabList {
      uid
      title
      isSelected
      scheme
      additionalString
      subTabList {
        uid
        title
        isSelected
        groupId
      }
    }
  }
  ... on ThemeKeywordSection {
    themeKeywordList {
      uid
      title
      scheme
    }
  }
  ... on StaticLandingDayOfWeekSection {
    isEnd
    totalCount
    param {
      categoryUid
      businessModel {
        name
        param
      }
      subcategory {
        name
        param
      }
      dayTab {
        name
        param
      }
      page
      size
      screenUid
    }
    businessModelList {
      name
      param
    }
    subcategoryList {
      name
      param
    }
    dayTabList {
      name
      param
    }
    promotionBanner {
      ...PromotionBannerItem
    }
  }
  ... on StaticLandingTodayNewSection {
    totalCount
    param {
      categoryUid
      subcategory {
        name
        param
      }
      screenUid
    }
    categoryTabList {
      name
      param
    }
    subcategoryList {
      name
      param
    }
    promotionBanner {
      ...PromotionBannerItem
    }
    viewType
  }
  ... on StaticLandingTodayUpSection {
    isEnd
    totalCount
    param {
      categoryUid
      subcategory {
        name
        param
      }
      page
    }
    categoryTabList {
      name
      param
    }
    subcategoryList {
      name
      param
    }
  }
  ... on StaticLandingRankingSection {
    isEnd
    rankingTime
    totalCount
    param {
      categoryUid
      subcategory {
        name
        param
      }
      rankingType {
        name
        param
      }
      page
      screenUid
    }
    categoryTabList {
      name
      param
    }
    subcategoryList {
      name
      param
    }
    rankingTypeList {
      name
      param
    }
    displayAd {
      ...DisplayAd
    }
    promotionBanner {
      ...PromotionBannerItem
    }
    withOperationArea
    viewType
  }
  ... on StaticLandingGenreSection {
    isEnd
    totalCount
    param {
      categoryUid
      subcategory {
        name
        param
      }
      sortType {
        name
        param
      }
      page
      isComplete
      screenUid
    }
    subcategoryList {
      name
      param
    }
    sortTypeList {
      name
      param
    }
    displayAd {
      ...DisplayAd
    }
    promotionBanner {
      ...PromotionBannerItem
    }
  }
  ... on StaticLandingFreeSeriesSection {
    isEnd
    totalCount
    param {
      categoryUid
      tab {
        name
        param
      }
      page
      screenUid
    }
    tabList {
      name
      param
    }
    promotionBanner {
      ...PromotionBannerItem
    }
  }
  ... on StaticLandingEventSection {
    isEnd
    totalCount
    param {
      categoryUid
      page
    }
    categoryTabList {
      name
      param
    }
  }
  ... on StaticLandingOriginalSection {
    isEnd
    totalCount
    originalCount
    param {
      categoryUid
      subcategory {
        name
        param
      }
      sortType {
        name
        param
      }
      isComplete
      page
      screenUid
    }
    subcategoryList {
      name
      param
    }
    sortTypeList {
      name
      param
    }
    recommendItemList {
      ...Item
    }
  }
  groups {
    ...Group
  }
}
    

    fragment PromotionBannerItem on PromotionBannerItem {
  title
  scheme
  leftImage
  rightImage
  eventLog {
    ...EventLogFragment
  }
}
    

    fragment EventLogFragment on EventLog {
  fromGraphql
  click {
    layer1
    layer2
    setnum
    ordnum
    copy
    imp_id
    imp_provider
  }
  eventMeta {
    id
    name
    subcategory
    category
    series
    provider
    series_id
    type
  }
  viewimp_contents {
    type
    name
    id
    imp_area_ordnum
    imp_id
    imp_provider
    imp_type
    layer1
    layer2
  }
  customProps {
    landing_path
    view_type
    toros_imp_id
    toros_file_hash_key
    toros_event_meta_id
    content_cnt
    event_series_id
    event_ticket_type
    play_url
    banner_uid
  }
}
    

    fragment DisplayAd on DisplayAd {
  sectionUid
  bannerUid
  treviUid
  momentUid
}
    

    fragment Item on Item {
  id
  type
  ...BannerItem
  ...OnAirItem
  ...CardViewItem
  ...CleanViewItem
  ... on DisplayAdItem {
    displayAd {
      ...DisplayAd
    }
  }
  ...PosterViewItem
  ...StrategyViewItem
  ...RankingListViewItem
  ...NormalListViewItem
  ...MoreItem
  ...EventBannerItem
  ...PromotionBannerItem
  ...LineBannerItem
}
    

    fragment BannerItem on BannerItem {
  bannerType
  bannerViewType
  thumbnail
  videoUrl
  badgeList
  statusBadge
  titleImage
  title
  altText
  metaList
  caption
  scheme
  seriesId
  eventLog {
    ...EventLogFragment
  }
  moreButton {
    ...MoreButtonFragment
  }
}
    

    fragment MoreButtonFragment on MoreButton {
  type
  scheme
  title
}
    

    fragment OnAirItem on OnAirItem {
  thumbnail
  videoUrl
  titleImage
  title
  subtitleList
  caption
  scheme
}
    

    fragment CardViewItem on CardViewItem {
  title
  altText
  thumbnail
  titleImage
  scheme
  badgeList
  ageGradeBadge
  statusBadge
  ageGrade
  selfCensorship
  torosImgId
  torosFileHashKey
  subtitleList
  caption
  rank
  rankVariation
  isEventBanner
  categoryType
  eventLog {
    ...EventLogFragment
  }
}
    

    fragment CleanViewItem on CleanViewItem {
  id
  type
  showPlayerIcon
  scheme
  title
  thumbnail
  badgeList
  ageGradeBadge
  statusBadge
  subtitleList
  rank
  torosFileHashKey
  torosImgId
  ageGrade
  selfCensorship
  eventLog {
    ...EventLogFragment
  }
}
    

    fragment PosterViewItem on PosterViewItem {
  id
  type
  showPlayerIcon
  scheme
  title
  altText
  thumbnail
  badgeList
  ageGradeBadge
  statusBadge
  subtitleList
  rank
  rankVariation
  torosFileHashKey
  torosImgId
  ageGrade
  selfCensorship
  eventLog {
    ...EventLogFragment
  }
  seriesId
}
    

    fragment StrategyViewItem on StrategyViewItem {
  id
  title
  count
  scheme
}
    

    fragment RankingListViewItem on RankingListViewItem {
  title
  thumbnail
  badgeList
  ageGradeBadge
  statusBadge
  ageGrade
  selfCensorship
  metaList
  descriptionList
  scheme
  torosImgId
  torosFileHashKey
  rank
  eventLog {
    ...EventLogFragment
  }
}
    

    fragment NormalListViewItem on NormalListViewItem {
  id
  type
  altText
  ticketUid
  thumbnail
  badgeList
  ageGradeBadge
  statusBadge
  ageGrade
  isAlaramOn
  row1
  row2
  row3 {
    id
    metaList
  }
  row4
  row5
  scheme
  continueScheme
  nextProductScheme
  continueData {
    ...ContinueInfoFragment
  }
  torosImpId
  torosFileHashKey
  seriesId
  isCheckMode
  isChecked
  isReceived
  showPlayerIcon
  rank
  isSingle
  singleSlideType
  ageGrade
  selfCensorship
  eventLog {
    ...EventLogFragment
  }
  giftEventLog {
    ...EventLogFragment
  }
}
    

    fragment ContinueInfoFragment on ContinueInfo {
  title
  isFree
  productId
  lastReadProductId
  scheme
  continueProductType
  hasNewSingle
  hasUnreadSingle
}
    

    fragment MoreItem on MoreItem {
  id
  scheme
  title
}
    

    fragment EventBannerItem on EventBannerItem {
  bannerType
  thumbnail
  videoUrl
  titleImage
  title
  subtitleList
  caption
  scheme
  eventLog {
    ...EventLogFragment
  }
}
    

    fragment LineBannerItem on LineBannerItem {
  title
  scheme
  subTitle
  bgColor
  rightImage
  eventLog {
    ...EventLogFragment
  }
}
    

    fragment Group on Group {
  id
  ... on ListViewGroup {
    meta {
      title
      count
    }
  }
  ... on CardViewGroup {
    meta {
      title
      count
    }
  }
  ... on PosterViewGroup {
    meta {
      title
      count
    }
  }
  type
  dataKey
  groups {
    ...GroupInGroup
  }
  items {
    ...Item
  }
}
    

    fragment GroupInGroup on Group {
  id
  type
  dataKey
  items {
    ...Item
  }
  ... on ListViewGroup {
    meta {
      title
      count
    }
  }
  ... on CardViewGroup {
    meta {
      title
      count
    }
  }
  ... on PosterViewGroup {
    meta {
      title
      count
    }
  }
}
"""

variables = {
    "sectionId": "static-landing-Genre-section-Layout-11-0-update-false-84",
    "param": {
        "categoryUid": 11,
        "subcategoryUid": "0",
        "sortType": "update", #latest, update
        "isComplete": False,
        "screenUid": 84,
        "page": 0
    }
}

def get_last_page_num():
    url = f"https://page.kakao.com/menu/10011/screen/84"
    page = requests.get(url)
    soup = bs(page.text, "lxml")
    last_page = soup.select(f"#__next > div > div.flex.w-full.grow.flex-col.px-122pxr > div > div.flex.grow.flex-col > div.mb-4pxr.flex-col > div > div.flex.h-44pxr.w-full.flex-row.items-center.justify-between.bg-bg-a-10.px-15pxr > div.flex.h-full.flex-1.items-center.space-x-8pxr > span")
    for element in last_page:
        total = element.text
    print(total)
    num = total.replace("개", "").replace(",", "")
    result = round(int(num) / 24)
    print(result)
    return result + 1

def get_novel_info_full(last_num):
    for page in range(0, last_num):
        variables["param"]["page"] = page

        data = {
            "query": query,
            "variables": variables
        }
        response = requests.post(
            url=url,
            headers=headers,
            json=data
        )

        sort_data(response, novel_list)

        print(f"Page {page} response:")
        time.sleep(1)

    store_info(novel_list)

novel_list = []
last_num = 10
#last_num = get_last_page_num()
get_novel_info_full(last_num)

"""
last_num = 10

for page in range(0, last_num):
    variables["param"]["page"] = page

    data = {
        "query": query,
        "variables": variables
    }
    response = requests.post(
        url=url,
        headers=headers,
        json=data
    )

    sort_data(response, novel_list)

    print(f"Page {page} response:")
    time.sleep(1)

store_info(novel_list)
"""