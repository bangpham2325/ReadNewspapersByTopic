<template>
  <div class="is-flex is-justify-content-center mt-4">
    <el-pagination
      background
      layout="prev, pager, next"
      :total="total"
      :current-page="+page"
      :page-size="+page_size"
      :pager-count="5"
      @current-change="$emit('change-page', $event)"
    />
  </div>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';

@Options({
  props: {
    total: Number,
    page: Number,
    page_size: Number
  }
})
export default class Pagination extends Vue {}
</script>

<style scoped>
:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active){
  background-color: #024547;
}
</style>