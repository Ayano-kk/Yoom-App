<template>
  <view class="container">
    <view class="header">
      <text class="title">我的收藏</text>
      <text class="sub">常用智能体与最近使用记录</text>
    </view>

    <view class="panel">
      <view class="panel-head">
        <text class="panel-title">收藏列表</text>
        <text class="panel-count">{{ favorites.length }} 个</text>
      </view>
      <view v-if="favorites.length" class="list-wrap">
        <view v-for="item in favorites" :key="item.agent_id" class="item-card">
          <image class="item-icon" :src="item.agent_icon" mode="aspectFill" />
          <view class="item-main">
            <text class="item-title">{{ item.agent_name }}</text>
            <text class="item-desc">{{ item.agent_desc }}</text>
          </view>
          <view class="item-action" @tap="showToast(`正在打开：${item.agent_name}`)">使用</view>
        </view>
      </view>
      <view v-else class="empty">暂未收藏，去智能体页面添加吧</view>
    </view>

    <view class="panel">
      <view class="panel-head">
        <text class="panel-title">最近使用</text>
        <text class="panel-count">{{ recent.length }} 条</text>
      </view>
      <view v-if="recent.length" class="chips">
        <view v-for="item in recent" :key="item.agent_id" class="chip">
          {{ item.agent_name }}
        </view>
      </view>
      <view v-else class="empty">暂无最近记录，先去体验一个智能体</view>
    </view>

    <BottomNav current="favorites" />
  </view>
</template>

<script setup>
import { onLoad, onPullDownRefresh } from "@dcloudio/uni-app";
import { ref } from "vue";
import BottomNav from "../../components/BottomNav.vue";
import { fetchFavorites, fetchRecent, login } from "../../services/api";

const FALLBACK_FAVORITES = [
  {
    agent_id: "local_copy_002",
    agent_name: "文案生成助手",
    agent_icon: "https://picsum.photos/seed/copy/160/160",
    agent_desc: "广告语、活动标题、社媒内容一键生成，灵感不断。"
  }
];

const FALLBACK_RECENT = [
  { agent_id: "local_service_001", agent_name: "智能客服助手" },
  { agent_id: "local_data_003", agent_name: "数据分析助手" }
];

const favorites = ref([]);
const recent = ref([]);

onLoad(async () => {
  try {
    await login();
  } catch (error) {}
  await loadData();
});

onPullDownRefresh(async () => {
  await loadData();
  uni.stopPullDownRefresh();
});

async function loadData() {
  await Promise.all([loadFavorites(), loadRecent()]);
}

async function loadFavorites() {
  try {
    const data = await fetchFavorites();
    favorites.value = data.items || [];
  } catch (error) {
    favorites.value = FALLBACK_FAVORITES;
  }
}

async function loadRecent() {
  try {
    const data = await fetchRecent();
    recent.value = data.items || [];
  } catch (error) {
    recent.value = FALLBACK_RECENT;
  }
}

function showToast(title) {
  uni.showToast({
    title,
    icon: "none"
  });
}
</script>

<style scoped>
.container {
  min-height: 100vh;
  padding: 0 24rpx 140rpx;
  background: #f5f8ff;
}

.header {
  margin: 0 -24rpx;
  padding: 82rpx 24rpx 34rpx;
  background: linear-gradient(90deg, #1b66ff 0%, #2f7bff 60%, #44a3ff 100%);
}

.title {
  display: block;
  color: #ffffff;
  font-size: 42rpx;
  font-weight: 600;
}

.sub {
  display: block;
  margin-top: 10rpx;
  color: rgba(255, 255, 255, 0.8);
  font-size: 24rpx;
}

.panel {
  margin-top: 20rpx;
  background: #ffffff;
  border-radius: 24rpx;
  border: 1rpx solid #f1f5f9;
  padding: 24rpx;
  box-shadow: 0 2rpx 24rpx rgba(15, 23, 42, 0.06);
}

.panel-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.panel-title {
  color: #334155;
  font-size: 30rpx;
  font-weight: 600;
}

.panel-count {
  color: #2f7bff;
  font-size: 22rpx;
}

.list-wrap {
  margin-top: 16rpx;
  display: flex;
  flex-direction: column;
  gap: 14rpx;
}

.item-card {
  background: #f8fbff;
  border-radius: 18rpx;
  padding: 16rpx;
  display: flex;
  align-items: center;
  gap: 14rpx;
}

.item-icon {
  width: 72rpx;
  height: 72rpx;
  border-radius: 16rpx;
  background: #dbeafe;
}

.item-main {
  flex: 1;
}

.item-title {
  display: block;
  color: #0f172a;
  font-size: 26rpx;
  font-weight: 600;
}

.item-desc {
  margin-top: 6rpx;
  display: block;
  color: #64748b;
  font-size: 22rpx;
}

.item-action {
  min-width: 92rpx;
  height: 56rpx;
  border-radius: 14rpx;
  color: #ffffff;
  background: #2f7bff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22rpx;
}

.chips {
  margin-top: 16rpx;
  display: flex;
  flex-wrap: wrap;
  gap: 12rpx;
}

.chip {
  padding: 10rpx 16rpx;
  border-radius: 999rpx;
  color: #1e40af;
  background: #dbeafe;
  font-size: 22rpx;
}

.empty {
  margin-top: 16rpx;
  color: #94a3b8;
  font-size: 22rpx;
}
</style>
