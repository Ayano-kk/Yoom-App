<template>
  <view class="bottom-nav">
    <view
      v-for="item in items"
      :key="item.key"
      class="nav-item"
      :class="{ active: current === item.key }"
      @tap="go(item)"
    >
      <text class="nav-icon">{{ item.icon }}</text>
      <text class="nav-label">{{ item.label }}</text>
    </view>
  </view>
</template>

<script setup>
const props = defineProps({
  current: {
    type: String,
    default: "home"
  }
});

const items = [
  { key: "home", label: "首页", icon: "🏠", path: "/pages/index/index" },
  { key: "agents", label: "智能体", icon: "🤖", path: "/pages/agents/index" },
  { key: "favorites", label: "收藏", icon: "⭐", path: "/pages/favorites/index" },
  { key: "profile", label: "我的", icon: "👤", path: "/pages/profile/index" }
];

function go(item) {
  if (props.current === item.key) {
    return;
  }
  uni.redirectTo({
    url: item.path
  });
}
</script>

<style scoped>
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
  z-index: 99;
}

.nav-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  color: #94a3b8;
}

.nav-item.active {
  color: #2f7bff;
}

.nav-icon {
  font-size: 34rpx;
}

.nav-label {
  margin-top: 8rpx;
  font-size: 20rpx;
}
</style>
