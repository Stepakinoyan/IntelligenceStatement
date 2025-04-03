<template>
  <div class="app">
    <header class="header">
      <img :src="gerb_rf" class="logo_pic" />
      <div class="logo">
        <h2>
          Интеллектуальное распознавание заявлений о внесении судебного приказа
        </h2>
        <button class="btn btn-primary">Все документы</button>
      </div>
    </header>
    <main>
      <router-view />
    </main>
  </div>
</template>

<script setup lang="ts">
import gerb_rf from "@/assets/gerb_rf.svg";
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
}

.header {
  display: flex;
  align-items: center;
  padding: 16px;
  background-color: #f5f5f5;
  border-bottom: 1px solid #ddd;
}

.logo {
  display: inline-block;
  align-items: bottom;
}

.logo h2 {
  @media (max-width: 480px) {
    font-size: medium;
  }
}

.logo_pic {
  width: 96px;
  margin-right: 32px;
  display: flex;
  align-items: center;
  justify-content: center;
}

main {
  flex: 1;
  padding: 1rem;
}
</style>
