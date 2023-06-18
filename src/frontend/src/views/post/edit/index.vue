<template>
<div class="form-layout">
	<el-row class="my-5">
		<el-col :span="12">
			<h2 class="title is-2">BÀI VIẾT</h2>
		</el-col>
		<el-col :span="12" class="is-flex is-justify-content-right">
			<el-tag size="large">Default</el-tag>
		</el-col>
	</el-row>

	<el-timeline>
		<el-timeline-item center timestamp="Tổng quát" placement="top">
			<el-card>
				<div class="field is-horizontal mt-4">
					<label class="title is-6 mr-3 mt-1">Tiêu đề:</label>
					<div class="field-body">
						<div class="field">
							<input class="input-field control" type="text">
						</div>
					</div>
				</div>

				<div class="field is-horizontal mt-4">
					<label class="title is-6 mr-3 mt-1">Tóm tắt:</label>
					<div class="field-body">
						<div class="field">
							<textarea class="textarea control" type="text"></textarea>
						</div>
					</div>
				</div>

				<div class="field is-horizontal">
					<label class="title is-6 mr-3">Thể loại:</label>
					<div class="field-body">
						<div class="field">
							<el-dropdown trigger="click">
								<span class="el-dropdown-link">
									{{ selectedCate }}<el-icon class="el-icon--right"><arrow-down /></el-icon>
								</span>
								<template #dropdown>
									<el-dropdown-menu v-for="opt in category" :key="opt">
										<el-dropdown-item @click="selectedCate=opt.title">{{opt.title}}</el-dropdown-item>
									</el-dropdown-menu>
								</template>
							</el-dropdown>
						</div>
					</div>
				</div>
			</el-card>
		</el-timeline-item>

		<el-timeline-item center timestamp="Chi tiết" placement="top">
			<el-card>
				<span class="title is-5 mt-3">
					Nội dung
					<button class="button is-light ml-2" style="font-size: 0.6rem" @click.prevent="expandEditor = true">
						<font-awesome-icon icon="fa-solid fa-up-right-and-down-left-from-center" class="mr-1"/> Expand
					</button>
				</span>

				<div :class="['mt-4', {expandEditor: expandEditor}]">
					<div :class="{expandEditor__content: expandEditor}">
						<TextEditor
							ref="editor"
							:is_freeze="is_freeze"
							:init_content="post.content"
							@contentChange="post.content = $event"
						/>
						<div class="is-flex is-justify-content-center">
							<button v-show="expandEditor" class="button is-rounded" @click.prevent="expandEditor = false">Close</button>
						</div>
					</div>
				</div>
			</el-card>
		</el-timeline-item>

		<el-timeline-item center timestamp="Gắn thẻ" placement="top">
			<el-card>
				<el-tag
					v-for="tag in dynamicTags"
					:key="tag"
					class="mx-1"
					closable
					:disable-transitions="false"
					@close="handleClose(tag)"
				>
					{{ tag }}
				</el-tag>
				<el-input
					v-if="inputVisible"
					v-model="inputValue"
					class="ml-1 w-20"
					style="width:150px;"
					:autofocus="true"
					size="small"
					@keyup.enter="handleInputConfirm"
					@blur="inputVisible=false"
				/>
				<el-button v-else class="button-new-tag ml-1" size="small" @click="inputVisible=true">
					+ New Tag
				</el-button>
			</el-card>
		</el-timeline-item>
	</el-timeline>
    
    <div class="is-flex is-justify-content-space-between">
      <button
        class="button is-success is-rounded"
        @click.prevent="handleSubmit($refs.formRef)"
        :disabled="is_freeze">
        <el-icon v-if="is_freeze" class="is-loading mr-2">
          <Loading/>
        </el-icon>
        Save
      </button>
      <button
        class="button is-dark is-rounded"
        @click.prevent="resetForm($refs.formRef)"
        :disabled="is_freeze">
        Reset
      </button>
    </div>
</div>
</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import TextEditor from "@/components/TextEditor.vue";
import {mapActions, mapMutations} from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';

@Options({
	components: {
    TextEditor,
  },

	data() {
    return {
			category: [],
			selectedCate: 'Click để chọn',
			inputValue: "",
			dynamicTags: [],
			inputVisible: false,
			focusInput: true,
      post: {
        title: "",
        content: "",
      },

			is_freeze: false,
      expandEditor: false,
    }
	},

  methods: {
		...mapMutations(["SET_LOADING"]),
    ...mapActions("topic", [ActionTypes.FETCH_TOPICS]),

		async getCategory(){
      this.SET_LOADING(true)
      let data = await this.FETCH_TOPICS()
      if (data) {
        this.category = data.results
      }
      this.SET_LOADING(false)
    },

		handleClose(tag: string){
			this.dynamicTags.splice(this.dynamicTags.indexOf(tag), 1)
		},

		handleInputConfirm (){
			if (this.inputValue) {
				this.dynamicTags.push(this.inputValue)
			}
			this.inputVisible = false
			this.inputValue = ''
		},
	},

	async created() {
    await this.getCategory()
  },
})

export default class EditPost extends Vue {
}
</script>

<style lang="scss" scoped>
.input-field {
  border: none;
  width: 100%;
  background-color: transparent;
	box-shadow: 0px 1px rgba(0, 0, 0, 0.2);
	&:focus {
		outline: none;
	}
}

.form-layout{
	padding: 0% 20% 0% 20%;
}
.expandEditor {
  position: fixed;
  top: -20px;
  left: 0;
  right: 0;
  bottom: 0;
  margin: 0;
  background-color: rgba(0, 0, 0, 0.5);
  z-index: 1999;
  transition: 0.3s all linear;

  &__content {
    position: fixed;
    top: 50%;
    left: 50%;
    z-index: 2000;
    padding: 20px;
    width: 90%;
    background-color: white;
    transform: translate(-50%, -50%);
    border-radius: 20px;
  }
}

</style>