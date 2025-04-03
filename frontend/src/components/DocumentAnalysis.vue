<template>
  <div class="document-list">
    <h3>Анализ документа</h3>
    <p>
      Документ проанализирован искусственным интеллектом, могут быть неточности
    </p>
    <table class="table table-striped">
      <tbody>
        <tr>
          <td>data</td>
          <td>data</td>
          <td>data</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup lang="ts">
import type { DocumentAnalysisData } from "@/api/api";

defineProps<{
  data: DocumentAnalysisData;
}>();
</script>
