<template>
  <div class="home">
    <div class="container">
      <button class="btn btn-primary" @click="$router.back()">Назад</button>
      <div class="btn-group" role="group">
        <button type="button" class="btn btn-success dropdown-toggle" @click="toggleDropdown">
          Скачать таблицу
        </button>
        <ul v-if="dropdownVisible" class="dropdown-menu">
          <li><button class="dropdown-item" @click="handleDownload('json')">Скачать JSON</button></li>
          <li><button class="dropdown-item" @click="handleDownload('excel')">Скачать Excel</button></li>
        </ul>
        <button type="button" class="btn btn-danger" @click="handleDelete">Удалить</button>
      </div>
      <DocumentAnalysis class="mt-4" v-if="analysisData" :data="analysisData" />
      <div v-else class="loading">
        <p>Загрузка анализа документа...</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import DocumentAnalysis from "@/components/DocumentAnalysis.vue";
import { useApi } from "@/api/api";
import type { DocumentAnalysisData } from "@/api/api";

const route = useRoute();
const router = useRouter();
const { fetchDocumentAnalysis, deleteDocumentById, downloadFileById } = useApi();
const analysisData = ref<DocumentAnalysisData | null>(null);
const documentId = ref<string>(String(route.params.id));
const dropdownVisible = ref<boolean>(false);

onMounted(async () => {
  try {
    analysisData.value = await fetchDocumentAnalysis(documentId.value);
  } catch (error) {
    console.error("Ошибка загрузки анализа документа:", error);
  }
});

const handleDelete = async () => {
  try {
    await deleteDocumentById(documentId.value);
    router.back();
  } catch (error) {
    console.error("Ошибка при удалении документа:", error);
  }
};

const handleDownload = async (type: "json" | "excel") => {
  try {
    await downloadFileById(Number(documentId.value), type);
    dropdownVisible.value = false; // Закрываем меню после выбора
  } catch (error) {
    console.error(`Ошибка при скачивании ${type}-файла:`, error);
  }
};

const toggleDropdown = () => {
  dropdownVisible.value = !dropdownVisible.value;
};
</script>

<style scoped>
.btn-group {
  position: relative;
}

.dropdown-menu {
  position: absolute;
  top: 100%;
  left: 0;
  z-index: 1000;
  display: block;
  background: white;
  border: 1px solid #ddd;
  border-radius: 4px;
  box-shadow: 0px 2px 5px rgba(0, 0, 0, 0.2);
  padding: 5px 0;
  min-width: 150px;
}

.dropdown-item {
  display: block;
  width: 100%;
  padding: 8px 16px;
  text-align: left;
  background: none;
  border: none;
  cursor: pointer;
}

.dropdown-item:hover {
  background: #f0f0f0;
}
</style>
