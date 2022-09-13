<template>
  <div class="editor-container">
    <QuillEditor
      v-model:content="content"
      ref="editor"
      contentType="html"
      :modules="modules"
      :toolbar="toolbarOptions"
      :enable="!is_freeze"
    />
  </div>
</template>

<script lang="ts">
import { Options, Vue } from "vue-class-component";
import { QuillEditor } from "@vueup/vue-quill";
import BlotFormatter from 'quill-blot-formatter'

@Options({
  components: {
    QuillEditor
  },
  props: {
    is_freeze: { type: Boolean, default: false },
    init_content: { type: String, default: ""},
  },
  data() {
    return {
      content: "",
      modules: {
        name: 'blotFormatter',
        module: BlotFormatter,
        options: {/* options */}
      } as any,
      toolbarOptions: [
          ['bold', 'italic', 'underline', 'strike'],        // toggled buttons
          ['blockquote', 'code-block'],

          [{'header': 1}, {'header': 2}],                   // custom button values
          [{'list': 'ordered'}, {'list': 'bullet'}],
          [{'script': 'sub'}, {'script': 'super'}],         // superscript/subscript
          [{'indent': '-1'}, {'indent': '+1'}],             // outdent/indent
        [{'direction': 'rtl'}],                             // text direction

          [{'size': ['small', false, 'large', 'huge']}],    // custom dropdown
          [{'header': [1, 2, 3, 4, 5, 6, false]}],
          [ 'link', 'video', 'image', 'formula' ],
          [{'color': []}, {'background': []}],              // dropdown with defaults from theme
          [{'font': []}],
          [{'align': []}],

          ['clean']                                         // remove formatting button
        ]
    }
  },
  watch: {
    content() {
      this.$emit('contentChange', this.content)
    }
  },
  created() {
    this.unwatchInitContent = this.$watch('init_content', (newVal: any) => {
      if (newVal) {
        this.content = newVal
        this.$refs.editor.getQuill().enable(false)
        this.$refs.editor.setHTML(this.content)
        this.$refs.editor.getQuill().enable(true)
        this.unwatchInitContent();
      }
    });
  }
})

export default class AddCampaignPage extends Vue {
  is_freeze!: boolean;
}
</script>

<style lang="scss" scoped>
.editor-container {
  min-height: 300px;
  max-height: fit-content;
  margin-bottom: 30px;
  border-radius: 20px;

  :deep(.ql-toolbar) {
    border-radius: 4px 4px 0px 0px;
  }

  :deep(.ql-container) {
    border-radius: 0px 0px 4px 4px;
    border: 1px solid #d1d5db;
  }

  :deep(.ql-editor) {
    min-height: 400px !important;
    max-height: 70vh !important;
    overflow: auto;
    color: black;
  }
}
</style>