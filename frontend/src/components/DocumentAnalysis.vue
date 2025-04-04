<template>
  <div class="document-list">
    <h3>Анализ документа</h3>
    <p>
      Документ проанализирован искусственным интеллектом, могут быть неточности
    </p>
    <table class="table table-striped">
      <tbody>
        <tr
          v-for="([key, value], index) in Object.entries(data.data)"
          :key="index"
        >
          <td>
            <strong>{{ key }}</strong>
          </td>
          <td v-if="Array.isArray(value)">
            <ul>
              <li v-for="(item, i) in value" :key="i">{{ item }}</li>
            </ul>
          </td>
          <td v-else>{{ value }}</td>
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
