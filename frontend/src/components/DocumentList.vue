<template>
  <div class="document-list">
    <h3>Недавние документы</h3>
    <p>Нажмите на строку, чтобы перейти к документу</p>
    <table class="table table-striped">
      <thead>
        <tr>
          <th scope="col">#</th>
          <th scope="col">Дата загрузки документа</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="doc in documents"
          :key="doc.id"
          @click="navigateToAnalysis(doc.id.toString())"
          class="document-item"
        >
          <td>{{ doc.id }}</td>
          <td>{{ formatDate(doc.create_at) }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import { useRouter } from "vue-router";
import type { DocumentPreview } from "@/api/api";

defineProps<{
  documents: DocumentPreview[];
}>();

const router = useRouter();

const navigateToAnalysis = (id: string) => {
  router.push({ name: "analysis", params: { id } });
};

const formatDate = (date: Date) => {
  return new Date(date).toLocaleDateString();
};
</script>

<style>
.document-item {
  cursor: pointer;
}
</style>
