<template>
<div class="form-layout" v-loading="loading">
	<el-row class="my-5">
		<el-col :span="12">
			<h2 class="title is-2">BÀI VIẾT</h2>
		</el-col>
		<el-col :span="12" class="is-flex is-justify-content-right">
			<el-tag size="large">DRAFT</el-tag>
		</el-col>
	</el-row>

	<el-timeline>
		<el-timeline-item center timestamp="Ảnh bìa" placement="top">
      <CoverImage
        :image="image"
        :is_freeze="is_freeze"
        @changeImage="this.image = $event"
        @changeFile="this.background = $event"
      >
      </CoverImage>
    </el-timeline-item>

		<el-timeline-item center timestamp="Tổng quát" placement="top">
			<el-card>
				<div class="field is-horizontal mt-4">
					<label class="title is-6 mr-3 mt-1">Tiêu đề:</label>
					<div class="field-body">
						<div class="field">
							<input class="input-field control" type="text" v-model="title">
						</div>
					</div>
				</div>

				<div class="field is-horizontal mt-4">
					<label class="title is-6 mr-3 mt-1">Tóm tắt:</label>
					<div class="field-body">
						<div class="field">
							<textarea class="textarea control" type="text" v-model="summary"></textarea>
						</div>
					</div>
				</div>

				<div class="field is-horizontal">
					<label class="title is-6 mr-3">Thể loại:</label>
					<div class="field-body">
						<div class="field">
							<el-dropdown trigger="click">
								<span class="el-dropdown-link">
									{{ selectedCate.title }}<el-icon class="el-icon--right"><arrow-down /></el-icon>
								</span>
								<template #dropdown>
									<el-dropdown-menu v-for="opt in category" :key="opt">
										<el-dropdown-item @click="selectedCate=opt">{{opt.title}}</el-dropdown-item>
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
						<font-awesome-icon icon="fa-solid fa-up-right-and-down-left-from-center" class="mr-1"/> Mở rộng
					</button>
				</span>

				<div :class="['mt-4', {expandEditor: expandEditor}]">
					<div :class="{expandEditor__content: expandEditor}">
						<TextEditor
							:is_freeze="is_freeze"
							:init_content="this.content"
							@contentChange="this.content = $event"
						/>
						<div class="is-flex is-justify-content-center">
							<button v-show="expandEditor" class="button is-rounded" @click.prevent="expandEditor = false">Đóng</button>
						</div>
					</div>
				</div>
			</el-card>
		</el-timeline-item>

		<el-timeline-item center timestamp="Gắn thẻ" placement="top">
			<el-card>
				<el-tag
					v-for="tag in hashTag"
					:key="tag"
					class="mx-1"
					closable
					:disable-transitions="false"
					@close="handleClose(tag)"
				>
					{{ tag.keyword }}
				</el-tag>
				<el-input
					v-if="inputVisible"
					v-model="inputValue"
					class="ml-1 w-20"
					style="width:150px;"
					autofocus="true"
					size="small"
					@keyup.enter="handleInputConfirm"
					@blur="inputVisible=false"
				/>
				<el-button v-else class="button-new-tag ml-1" size="small" @click="inputVisible=true">
					+ Thêm Tag
				</el-button>
			</el-card>
		</el-timeline-item>
	</el-timeline>
    
	<div class="is-flex is-justify-content-space-between">
		<button
			class="button is-dark is-rounded"
			@click.prevent="UserPost('ADD')"
			:disabled="is_freeze">
			<el-icon v-if="is_freeze" class="is-loading mr-2">
				<Loading/>
			</el-icon>
			Lưu bài viết
		</button>
		<button
			class="button is-success is-rounded"
			@click.prevent="UserPost('PUBLISH')"
			:disabled="is_freeze">
			Đăng bài viết
		</button>
	</div>
</div>

<div v-loading="loading">
	<el-affix position="bottom" :offset="70">
		<div class="is-flex is-justify-content-right">
			<el-tooltip content="Preview" placement="top-start">
				<el-button :disabled="!title || !selectedCate.id" type="info" icon="Tickets" circle @click="previewPost=true" size="large"/>
			</el-tooltip>
		</div>
	</el-affix>

	<el-dialog v-model="previewPost" width="70%">
		<div style="margin-bottom:50px;">
      <p class="title is-5" style="color:#00773e">{{selectedCate.title }}</p>
			<h1 class="title is-2">{{ title }}</h1>
			<p class="subtitle is-5 mt-1" style="color:#808080">{{ summary }}</p>
			<el-row>
				<el-col :span="12">
					<el-row>
						<el-avatar :size="50">
							<img :src="userInfo.avatar"
								style="object-fit: contain;">
						</el-avatar>
						<el-tooltip content="Bài viết của tác giả" placement="top-start">
							<a class="title is-6 mt-4 ml-4" style="color:#00773e;">
							{{ userInfo.full_name }}
							</a>
						</el-tooltip>
					</el-row>
				</el-col>
			</el-row>
		</div>

    <div>
      <div v-html="content"></div>
    </div>
    <div>
      <el-row>
				<el-col :span="12">
					<el-tag class="mr-4" size="large" v-for="tag in hashTag">{{ tag.keyword }}</el-tag>
				</el-col>
			</el-row>
    </div>
	</el-dialog>
</div>

</template>

<script lang="ts">
import {Options, Vue} from "vue-class-component";
import TextEditor from "@/components/TextEditor.vue";
import {mapActions, mapMutations, mapGetters} from "vuex";
import { ActionTypes } from '@/types/store/ActionTypes';
import CoverImage from "@/components/CoverImage.vue";
import { ElMessage } from "element-plus";

@Options({
	components: {
    TextEditor,
		CoverImage,
  },

	data() {
    return {
			category: [],
			title: '',
			summary: '',
			content: '',
			selectedCate: {
				id: '',
				title: 'Click để chọn'},
			inputValue: "",
			hashTag: [],
			inputVisible: false,
			is_freeze: false,
      expandEditor: false,
			loading: true,
			image: "",
      background: null,
			previewPost: false,
    }
	},

  methods: {
		...mapMutations(["SET_LOADING"]),
    ...mapActions("topic", [ActionTypes.FETCH_TOPICS]),
		...mapActions("post", [ActionTypes.ADD_USER_POST, ActionTypes.UPDATE_STATUS_POST]),

		async getCategory(){
      this.SET_LOADING(true)
      let data = await this.FETCH_TOPICS()
      if (data) {
        this.category = data.results
      }
      this.SET_LOADING(false)
    },

		handleClose(tag: string){
			this.hashTag.splice(this.hashTag.indexOf(tag), 1)
		},

		handleInputConfirm (){
			if (this.inputValue) {
				this.hashTag.push({keyword: this.inputValue})
			}
			this.inputVisible = false
			this.inputValue = ''
		},

		async UserPost(type: string){
			this.is_freeze = true
			let status = 0
			let formData = new FormData();

			formData.append("title", this.title);
			formData.append("summary", this.summary);
			formData.append("description", this.content);
			formData.append("category_ids", this.selectedCate.id);
			formData.append("thumbnail", this.background?.raw)

			this.hashTag.map((tag: any) => {
        formData.append("keywords", tag.keyword ? tag.keyword : "")
      })

			if(!this.selectedCate.id || !this.title){
        if(!this.title)
          ElMessage.warning('Vui lòng điền tiêu đề cho bài viết.')
        if(!this.selectedCate.id)
          ElMessage.warning('Vui lòng chọn thể loại cho bài viết.')
				if(!this.background)
					ElMessage.warning('Vui lòng tải ảnh nền cho bài viết.')
      }
      else{
        if(type == 'ADD'){
          let res: any = await this.ADD_USER_POST(formData)
          status = res.status
        }
        else {
          let res_data: any = await this.ADD_USER_POST(formData)
          let res = await this.UPDATE_STATUS_POST({ id: res_data.data.id, status: { status: 'PENDING' } })
          status = res.status
        }
      }
				
			if(status == 201 || status == 200)
				this.$router.push("/post/my-posts")

			this.is_freeze = false
		}
	},
	computed: {
		...mapGetters("user", ["userInfo"]),
	},

	async created() {
    await this.getCategory()
		this.loading = false

		this.unwatchPost = this.$watch('post', (newVal: any) => {
      if (newVal) {
        this.image = newVal.background
        this.unwatchPost();
      }
    });
  },
})

export default class AddPost extends Vue {
}
</script>

<style lang="scss" scoped>
:deep(.ql-align-center){
	text-align: center;
}

:deep(.ql-align-right){
	text-align: right;
}

:deep(.img-content p img){
  display: block;
  margin: auto auto;
}
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