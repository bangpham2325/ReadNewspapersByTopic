<template>
  <el-form
    ref="topicForm"
    size="large"
    :model="form"
    label-width="100px"
    @change="$emit('updateTopic', form)"
    :rules="rules"
  >
    <el-form-item label="Title" prop="title">
      <el-input v-model="form.name" placeholder="Enter title" autocomplete="off"/>
    </el-form-item>

    <el-form-item label="Description" prop="description">
      <el-input type="textarea" v-model="form.description" placeholder="Enter description..." autocomplete="off"/>
    </el-form-item>
  </el-form>
</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import TopicItem from "@/types/campaign/TopicItem";

@Options({
  props: {
    topic: {} as TopicItem
  },
  data(){
    return {
      form: {} as TopicItem,
      rules: {
        name: [
          {required: true, message: 'Please input title', trigger: 'blur'},
          {min: 5, max: 25, message: 'Length should be 5 to 25', trigger: ['blur', 'change']},
        ],
        description: [
          {required: true, message: 'Please input description', trigger: 'blur'},
          {max: 25, message: 'Maximum 150 words.', trigger: ['blur', 'change']},
        ]
      } as any,
    }
  },
  watch: {
    topic: {
      deep: true,
      handler: function(){
        this.form = {...this.topic}
      }
    }
  },
  created() {
    this.form = {...this.topic}
  }
})

export default class TopicForm extends Vue {}
</script>