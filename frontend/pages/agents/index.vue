<template>
  <view class="container">
    <view class="header">
      <text class="title">智能体广场</text>
      <text class="sub">按分类快速找到可用能力</text>
    </view>

    <view class="search-box">
      <text class="search-icon">🔍</text>
      <input
        v-model="keyword"
        class="search-input"
        placeholder="搜索智能体名称或关键词"
        confirm-type="search"
        @confirm="loadAgents"
      />
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
          <view class="action-primary" @tap="showToast(`正在打开：${agent.agent_name}`)">立即使用</view>
        </view>
      </view>
    </view>

    <BottomNav current="agents" />
  </view>
</template>

<script setup>
import { onLoad, onPullDownRefresh } from "@dcloudio/uni-app";
import { ref } from "vue";
import BottomNav from "../../components/BottomNav.vue";
import { addFavorite, fetchAgents, fetchFavorites, login, removeFavorite } from "../../services/api";

const FALLBACK_AGENTS = [
  {
    agent_id: "local_service_001",
    agent_name: "智能客服助手",
    agent_icon: "https://picsum.photos/seed/service/160/160",
    agent_desc: "7x24小时在线响应，自动解答常见问题并转人工。",
    category: "客服",
    is_hot: true
  },
  {
    agent_id: "local_copy_002",
    agent_name: "文案生成助手",
    agent_icon: "https://picsum.photos/seed/copy/160/160",
    agent_desc: "广告语、活动标题、社媒内容一键生成，灵感不断。",
    category: "文案",
    is_hot: false
  },
  {
    agent_id: "local_data_003",
    agent_name: "数据分析助手",
    agent_icon: "https://picsum.photos/seed/data/160/160",
    agent_desc: "自动洞察业务趋势，生成图表与摘要报告提升决策效率。",
    category: "数据",
    is_hot: false
  }
];

const agents = ref([]);
const categories = ref(["全部"]);
const activeCategory = ref("全部");
const keyword = ref("");
const favoriteIds = ref(new Set());

onLoad(async () => {
  try {
    await login();
  } catch (error) {}
  await Promise.all([loadAgents(), loadFavorites()]);
});

onPullDownRefresh(async () => {
  await Promise.all([loadAgents(), loadFavorites()]);
  uni.stopPullDownRefresh();
});

async function loadAgents() {
  try {
    const params = { page: 1, size: 30 };
    if (activeCategory.value !== "全部") {
      params.category = activeCategory.value;
    }
    if (keyword.value.trim()) {
      params.keyword = keyword.value.trim();
    }
    const data = await fetchAgents(params);
    applyAgentList(data.items || []);
  } catch (error) {
    const kw = keyword.value.trim().toLowerCase();
    const list = FALLBACK_AGENTS.filter((item) => {
      const byCategory = activeCategory.value === "全部" || item.category === activeCategory.value;
      const byKeyword = !kw || item.agent_name.toLowerCase().includes(kw) || item.agent_desc.toLowerCase().includes(kw);
      return byCategory && byKeyword;
    });
    applyAgentList(list);
  }
}

async function loadFavorites() {
  try {
    const data = await fetchFavorites();
    favoriteIds.value = new Set((data.items || []).map((item) => item.agent_id));
  } catch (error) {}
}

function applyAgentList(list) {
  agents.value = list;
  const sourceCategories = Array.from(new Set(list.map((item) => item.category)));
  categories.value = ["全部", ...sourceCategories];
}

function switchCategory(category) {
  activeCategory.value = category;
  loadAgents();
}

function isFavorite(agentId) {
  return favoriteIds.value.has(agentId);
}

async function toggleFavorite(agent) {
  try {
    if (favoriteIds.value.has(agent.agent_id)) {
      await removeFavorite(agent.agent_id);
      favoriteIds.value.delete(agent.agent_id);
      showToast("已取消收藏");
      return;
    }
    await addFavorite(agent.agent_id);
    favoriteIds.value.add(agent.agent_id);
    showToast("收藏成功");
  } catch (error) {
    if (favoriteIds.value.has(agent.agent_id)) {
      favoriteIds.value.delete(agent.agent_id);
      showToast("已取消收藏");
      return;
    }
    favoriteIds.value.add(agent.agent_id);
    showToast("收藏成功");
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

.search-box {
  margin-top: -16rpx;
  height: 84rpx;
  border-radius: 24rpx;
  background: #ffffff;
  display: flex;
  align-items: center;
  padding: 0 24rpx;
  box-shadow: 0 2rpx 24rpx rgba(15, 23, 42, 0.06);
}

.search-icon {
  margin-right: 10rpx;
}

.search-input {
  flex: 1;
  font-size: 26rpx;
}

.category-scroll {
  margin-top: 26rpx;
  white-space: nowrap;
}

.category-list {
  display: inline-flex;
  align-items: center;
  gap: 22rpx;
}

.category-item {
  font-size: 24rpx;
  color: #64748b;
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
</style>
