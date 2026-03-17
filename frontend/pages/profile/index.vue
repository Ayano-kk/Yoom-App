<template>
  <view class="container">
    <view class="header">
      <text class="title">我的</text>
      <text class="sub">账号信息与使用概览</text>
    </view>

    <view class="profile-card">
      <view class="avatar">{{ avatarText }}</view>
      <view class="profile-main">
        <text class="name">{{ profile.nickname || "微信用户" }}</text>
        <text class="desc">欢迎回来，继续高效完成你的工作</text>
      </view>
    </view>

    <view class="stats">
      <view class="stat-item">
        <text class="stat-value">{{ summary.favoriteCount }}</text>
        <text class="stat-label">收藏数</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ summary.recentCount }}</text>
        <text class="stat-label">最近使用</text>
      </view>
      <view class="stat-item">
        <text class="stat-value">{{ summary.totalAgents }}</text>
        <text class="stat-label">智能体总量</text>
      </view>
    </view>

    <view class="menu-card">
      <view class="menu-item" @tap="showToast('账号设置建设中')">
        <text>账号设置</text>
        <text>›</text>
      </view>
      <view class="menu-item" @tap="showToast('消息通知建设中')">
        <text>消息通知</text>
        <text>›</text>
      </view>
      <view class="menu-item" @tap="showToast('帮助反馈建设中')">
        <text>帮助反馈</text>
        <text>›</text>
      </view>
    </view>

    <BottomNav current="profile" />
  </view>
</template>

<script setup>
import { computed, reactive } from "vue";
import { onLoad, onPullDownRefresh } from "@dcloudio/uni-app";
import BottomNav from "../../components/BottomNav.vue";
import { fetchAgents, fetchFavorites, fetchRecent, login } from "../../services/api";
import { getProfile } from "../../utils/request";

const profile = reactive(getProfile());
const summary = reactive({
  favoriteCount: 0,
  recentCount: 0,
  totalAgents: 0
});

const avatarText = computed(() => {
  const name = profile.nickname || "微信用户";
  return name.slice(0, 1);
});

onLoad(async () => {
  try {
    await login();
  } catch (error) {}
  Object.assign(profile, getProfile());
  await loadSummary();
});

onPullDownRefresh(async () => {
  await loadSummary();
  uni.stopPullDownRefresh();
});

async function loadSummary() {
  try {
    const [favoriteRes, recentRes, agentRes] = await Promise.all([
      fetchFavorites(),
      fetchRecent(),
      fetchAgents({ page: 1, size: 1 })
    ]);
    summary.favoriteCount = (favoriteRes.items || []).length;
    summary.recentCount = (recentRes.items || []).length;
    summary.totalAgents = agentRes.total || (agentRes.items || []).length;
  } catch (error) {
    summary.favoriteCount = 1;
    summary.recentCount = 2;
    summary.totalAgents = 6;
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

.profile-card {
  margin-top: 20rpx;
  background: #ffffff;
  border-radius: 24rpx;
  border: 1rpx solid #f1f5f9;
  box-shadow: 0 2rpx 24rpx rgba(15, 23, 42, 0.06);
  padding: 24rpx;
  display: flex;
  align-items: center;
  gap: 16rpx;
}

.avatar {
  width: 96rpx;
  height: 96rpx;
  border-radius: 50%;
  background: linear-gradient(135deg, #2f7bff 0%, #44a3ff 100%);
  color: #ffffff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 42rpx;
  font-weight: 600;
}

.profile-main {
  flex: 1;
}

.name {
  display: block;
  color: #0f172a;
  font-size: 30rpx;
  font-weight: 600;
}

.desc {
  display: block;
  margin-top: 8rpx;
  color: #64748b;
  font-size: 22rpx;
}

.stats {
  margin-top: 18rpx;
  display: flex;
  gap: 14rpx;
}

.stat-item {
  flex: 1;
  background: #ffffff;
  border-radius: 20rpx;
  border: 1rpx solid #f1f5f9;
  box-shadow: 0 2rpx 24rpx rgba(15, 23, 42, 0.06);
  padding: 18rpx 12rpx;
  text-align: center;
}

.stat-value {
  display: block;
  color: #1e40af;
  font-size: 34rpx;
  font-weight: 700;
}

.stat-label {
  display: block;
  margin-top: 6rpx;
  color: #64748b;
  font-size: 20rpx;
}

.menu-card {
  margin-top: 18rpx;
  background: #ffffff;
  border-radius: 24rpx;
  border: 1rpx solid #f1f5f9;
  box-shadow: 0 2rpx 24rpx rgba(15, 23, 42, 0.06);
  overflow: hidden;
}

.menu-item {
  height: 90rpx;
  padding: 0 24rpx;
  display: flex;
  align-items: center;
  justify-content: space-between;
  color: #334155;
  font-size: 26rpx;
  border-bottom: 1rpx solid #eef2ff;
}

.menu-item:last-child {
  border-bottom: none;
}
</style>
