<template>
  <view class="container">
    <view class="header">
      <text class="title">沄荣科技</text>
      <view class="ai-btn" @tap="showToast('AI助手功能建设中')">🤖 AI助手</view>
    </view>

    <view class="search-wrap">
      <view class="search-box">
        <text class="search-icon">🔍</text>
        <input
          v-model="keyword"
          class="search-input"
          placeholder="搜索智能体 / 关键词搜索"
          confirm-type="search"
          @confirm="handleSearch"
        />
      </view>
    </view>

    <view class="recommend-card">
      <text class="recommend-tag">AI RECOMMEND</text>
      <text class="recommend-title">{{ topRecommendation.agent?.agent_name || "积墨AI智能体推荐" }}</text>
      <text class="recommend-desc">{{ topRecommendation.agent?.agent_desc || "高效协作 · 快速生成 · 企业级能力" }}</text>
    </view>

    <scroll-view class="category-scroll" scroll-x>
      <view class="category-list">
        <view
          v-for="item in categories"
          :key="item"
          class="category-item"
          :class="{ active: activeCategory === item }"
          @tap="switchCategory(item)"
        >
          {{ item }}
        </view>
      </view>
    </scroll-view>

    <view class="agent-list">
      <view v-for="agent in agents" :key="agent.agent_id" class="agent-card">
        <view class="agent-main">
          <image class="agent-icon" :src="agent.agent_icon" mode="aspectFill" />
          <view class="agent-content">
            <view class="agent-title-row">
              <text class="agent-title">{{ agent.agent_name }}</text>
              <text v-if="agent.is_hot" class="badge-hot">热门</text>
              <text v-else class="badge-normal">{{ agent.category }}</text>
            </view>
            <text class="agent-desc">{{ agent.agent_desc }}</text>
          </view>
        </view>
        <view class="agent-actions">
          <view class="action-light" @tap="toggleFavorite(agent)">
            {{ isFavorite(agent.agent_id) ? "取消收藏" : "收藏" }}
          </view>
          <view class="action-primary" @tap="openAgent(agent)">立即使用</view>
        </view>
      </view>
    </view>

    <view class="recommend-actions">
      <view class="action-outline" @tap="showToast('已减少推荐位（演示）')">减少</view>
      <view class="action-fill" @tap="showToast('已新增推荐位（演示）')">新增</view>
    </view>

    <view class="card-panel">
      <text class="panel-title">收藏</text>
      <text class="panel-desc">{{ favoritesSummary }}</text>
    </view>

    <view class="card-panel profile">
      <text class="panel-title">我的</text>
      <text class="panel-desc">当前登录：{{ profile.nickname || "微信用户" }}</text>
    </view>

    <view class="bottom-nav">
      <view class="nav-item nav-active">
        <text class="nav-icon">🏠</text>
        <text class="nav-label">首页</text>
      </view>
      <view class="nav-item" @tap="showToast('智能体模块建设中')">
        <text class="nav-icon">🤖</text>
        <text class="nav-label">智能体</text>
      </view>
      <view class="nav-item" @tap="showToast('收藏模块建设中')">
        <text class="nav-icon">⭐</text>
        <text class="nav-label">收藏</text>
      </view>
      <view class="nav-item" @tap="showToast('我的模块建设中')">
        <text class="nav-icon">👤</text>
        <text class="nav-label">我的</text>
      </view>
    </view>
  </view>
</template>

<script setup>
import { computed, ref } from "vue";
import { onLoad, onPullDownRefresh } from "@dcloudio/uni-app";
import {
  addFavorite,
  fetchAgents,
  fetchFavorites,
  fetchRecommendations,
  login,
  removeFavorite
} from "../../services/api";
import { getProfile } from "../../utils/request";

const agents = ref([]);
const categories = ref(["全部"]);
const activeCategory = ref("全部");
const keyword = ref("");
const topRecommendation = ref({});
const favoriteIds = ref(new Set());
const favorites = ref([]);
const profile = ref(getProfile());

const favoritesSummary = computed(() => {
  if (!favorites.value.length) {
    return "暂无收藏，去挑选你感兴趣的智能体吧";
  }
  const names = favorites.value.slice(0, 3).map((item) => item.agent_name);
  return `已收藏 ${favorites.value.length} 个：${names.join("、")}`;
});

async function initPage() {
  try {
    await login();
    profile.value = getProfile();
  } catch (error) {
    showToast(error.message || "登录失败");
  }
  await Promise.all([loadRecommendations(), loadAgents(), loadFavorites()]);
}

async function loadRecommendations() {
  try {
    const data = await fetchRecommendations();
    topRecommendation.value = data.items?.[0] || {};
  } catch (error) {
    showToast(error.message || "推荐位加载失败");
  }
}

async function loadAgents() {
  try {
    const params = { page: 1, size: 20 };
    if (activeCategory.value !== "全部") {
      params.category = activeCategory.value;
    }
    if (keyword.value.trim()) {
      params.keyword = keyword.value.trim();
    }
    const data = await fetchAgents(params);
    agents.value = data.items || [];
    const sourceCategories = Array.from(new Set((data.items || []).map((item) => item.category)));
    categories.value = ["全部", ...sourceCategories];
  } catch (error) {
    showToast(error.message || "智能体加载失败");
  } finally {
    uni.stopPullDownRefresh();
  }
}

async function loadFavorites() {
  try {
    const data = await fetchFavorites();
    favorites.value = data.items || [];
    favoriteIds.value = new Set((data.items || []).map((item) => item.agent_id));
  } catch (error) {
    favorites.value = [];
    favoriteIds.value = new Set();
  }
}

async function toggleFavorite(agent) {
  try {
    if (favoriteIds.value.has(agent.agent_id)) {
      await removeFavorite(agent.agent_id);
      showToast("已取消收藏");
    } else {
      await addFavorite(agent.agent_id);
      showToast("收藏成功");
    }
    await loadFavorites();
  } catch (error) {
    showToast(error.message || "收藏操作失败");
  }
}

function isFavorite(agentId) {
  return favoriteIds.value.has(agentId);
}

function openAgent(agent) {
  if (agent.jump_url) {
    showToast(`正在打开：${agent.agent_name}`);
    return;
  }
  showToast("智能体链接暂不可用");
}

function switchCategory(category) {
  activeCategory.value = category;
  loadAgents();
}

function handleSearch() {
  loadAgents();
}

function showToast(title) {
  uni.showToast({
    title,
    icon: "none"
  });
}

onLoad(() => {
  initPage();
});

onPullDownRefresh(() => {
  Promise.all([loadRecommendations(), loadAgents(), loadFavorites()]);
});
</script>

<style scoped>
.container {
  min-height: 100vh;
  padding: 0 24rpx 140rpx;
}

.header {
  background: linear-gradient(90deg, #1b66ff 0%, #2f7bff 60%, #44a3ff 100%);
  margin: 0 -24rpx;
  padding: 80rpx 24rpx 36rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.title {
  color: #ffffff;
  font-size: 42rpx;
  font-weight: 600;
}

.ai-btn {
  border: 1rpx solid rgba(255, 255, 255, 0.3);
  background: rgba(255, 255, 255, 0.18);
  color: #ffffff;
  font-size: 24rpx;
  border-radius: 999rpx;
  padding: 10rpx 24rpx;
}

.search-wrap {
  margin-top: -18rpx;
}

.search-box {
  height: 84rpx;
  background: #ffffff;
  border-radius: 24rpx;
  padding: 0 24rpx;
  display: flex;
  align-items: center;
  box-shadow: 0 2rpx 24rpx rgba(15, 23, 42, 0.06);
}

.search-icon {
  margin-right: 10rpx;
  color: #94a3b8;
}

.search-input {
  flex: 1;
  font-size: 26rpx;
}

.recommend-card {
  margin-top: 24rpx;
  border-radius: 30rpx;
  background: linear-gradient(135deg, #0b1636 0%, #132a5a 55%, #1c3b7a 100%);
  color: #ffffff;
  padding: 34rpx;
  box-shadow: 0 16rpx 48rpx rgba(16, 24, 40, 0.12);
}

.recommend-tag {
  color: #67e8f9;
  font-size: 18rpx;
  letter-spacing: 6rpx;
}

.recommend-title {
  display: block;
  margin-top: 12rpx;
  font-size: 38rpx;
  font-weight: 700;
}

.recommend-desc {
  display: block;
  margin-top: 14rpx;
  color: rgba(255, 255, 255, 0.72);
  font-size: 24rpx;
}

.category-scroll {
  margin-top: 26rpx;
  white-space: nowrap;
}

.category-list {
  display: inline-flex;
  align-items: center;
  gap: 24rpx;
  padding-bottom: 8rpx;
}

.category-item {
  color: #64748b;
  font-size: 25rpx;
  padding: 6rpx 0;
  border-bottom: 5rpx solid transparent;
}

.category-item.active {
  color: #2f7bff;
  font-weight: 600;
  border-bottom-color: #2f7bff;
}

.agent-list {
  margin-top: 18rpx;
  display: flex;
  flex-direction: column;
  gap: 18rpx;
}

.agent-card {
  background: #ffffff;
  border-radius: 26rpx;
  padding: 26rpx;
  border: 1rpx solid #f1f5f9;
  box-shadow: 0 12rpx 30rpx rgba(16, 24, 40, 0.06);
}

.agent-main {
  display: flex;
  gap: 16rpx;
}

.agent-icon {
  width: 88rpx;
  height: 88rpx;
  border-radius: 20rpx;
  background: #f1f5f9;
}

.agent-content {
  flex: 1;
}

.agent-title-row {
  display: flex;
  align-items: center;
  gap: 10rpx;
}

.agent-title {
  font-size: 30rpx;
  color: #1e293b;
  font-weight: 600;
}

.badge-hot {
  font-size: 18rpx;
  color: #f97316;
  background: #ffedd5;
  border-radius: 999rpx;
  padding: 4rpx 12rpx;
}

.badge-normal {
  font-size: 18rpx;
  color: #2563eb;
  background: #dbeafe;
  border-radius: 999rpx;
  padding: 4rpx 12rpx;
}

.agent-desc {
  margin-top: 10rpx;
  color: #64748b;
  font-size: 24rpx;
  line-height: 1.5;
}

.agent-actions {
  margin-top: 22rpx;
  display: flex;
  justify-content: flex-end;
  gap: 16rpx;
}

.action-light {
  height: 68rpx;
  border-radius: 18rpx;
  padding: 0 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #2f7bff;
  border: 1rpx solid #2f7bff;
  font-size: 24rpx;
}

.action-primary {
  height: 68rpx;
  border-radius: 18rpx;
  padding: 0 24rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  background: #2f7bff;
  font-size: 24rpx;
}

.card-panel {
  margin-top: 20rpx;
  background: #ffffff;
  border-radius: 24rpx;
  border: 1rpx solid #f1f5f9;
  box-shadow: 0 2rpx 24rpx rgba(15, 23, 42, 0.06);
  padding: 24rpx;
}

.profile {
  margin-bottom: 18rpx;
}

.recommend-actions {
  margin-top: 22rpx;
  display: flex;
  gap: 16rpx;
}

.action-outline {
  flex: 1;
  height: 74rpx;
  border-radius: 999rpx;
  border: 1rpx solid #2f7bff;
  color: #2f7bff;
  background: #ffffff;
  font-size: 25rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.action-fill {
  flex: 1;
  height: 74rpx;
  border-radius: 999rpx;
  color: #ffffff;
  background: #2f7bff;
  font-size: 25rpx;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: 600;
}

.bottom-nav {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  height: 112rpx;
  background: #ffffff;
  border-top: 1rpx solid #f1f5f9;
  display: flex;
  align-items: center;
  justify-content: space-around;
  box-shadow: 0 -8rpx 24rpx rgba(15, 23, 42, 0.05);
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #94a3b8;
}

.nav-active {
  color: #2f7bff;
}

.nav-icon {
  font-size: 34rpx;
}

.nav-label {
  margin-top: 8rpx;
  font-size: 20rpx;
}

.panel-title {
  font-size: 28rpx;
  color: #334155;
  font-weight: 600;
}

.panel-desc {
  display: block;
  margin-top: 10rpx;
  font-size: 22rpx;
  color: #94a3b8;
  line-height: 1.5;
}
</style>
