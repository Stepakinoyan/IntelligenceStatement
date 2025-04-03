<template>
  <div class="home">
    <div class="container">
      <button class="btn btn-primary" @click="$router.back()">Назад</button>
      <div class="btn-group" role="group">
        <button type="button" class="btn btn-primary">
          Скачать исходный PDF
        </button>
        <button type="button" class="btn btn-success">
          Скачать таблицу как JSON файл
        </button>
        <button type="button" class="btn btn-danger">Удалить</button>
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
import { useRoute } from "vue-router";
import DocumentAnalysis from "@/components/DocumentAnalysis.vue";
import { useApi } from "@/api/api";
import type { DocumentAnalysisData } from "@/api/api";

const route = useRoute();
const { fetchDocumentAnalysis } = useApi();
const analysisData = ref<DocumentAnalysisData | null>(null);

onMounted(async () => {
  const documentId = route.params.id as string;
  analysisData.value = await fetchDocumentAnalysis(documentId);
});
</script>

<style scoped>
.btn-group {
  @media (max-width: 480px) {
    margin-left: 0px;
  }
  @media (min-width: 480px) {
    margin-left: 8px;
  }
}
</style>
