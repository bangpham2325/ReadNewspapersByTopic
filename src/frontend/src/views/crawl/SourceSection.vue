<template>
<el-tooltip
	class="box-item"
	content="click vào để chọn hoặc bỏ chọn"
	placement="top"
>
  <el-descriptions :column="2" border :class="['mb-5', {'selectedSource': selectedSource.includes('Vietnamnet')}]" @click="clickSource('Vietnamnet')">
		<el-descriptions-item min-width="120">
			<template #label>
				<div><el-icon><user /></el-icon>Trang</div>
			</template>
			Vietnamnet
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div><el-icon><iphone /></el-icon>Link</div>
			</template>
			<a href="https://vietnamnet.vn/" target="blank">https://vietnamnet.vn/</a>
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div><el-icon><tickets /></el-icon>Giới thiệu</div>
			</template>
			Vietnamnet là một trong những trang thông tin điện tử hàng đầu tại Việt Nam. Với nền tảng truyền thông đa dạng, Vietnamnet cung cấp cho người đọc những tin tức, bài viết đa dạng về chính trị, kinh tế, xã hội, văn hóa, thể thao và nhiều lĩnh vực khác. Với uy tín và chất lượng thông tin, Vietnamnet là một nguồn tin đáng tin cậy và được đông đảo người dùng Việt Nam tin tưởng và theo dõi.
		</el-descriptions-item>
	</el-descriptions>
</el-tooltip>

	<el-descriptions :column="2" border :class="['mb-5', {'selectedSource': selectedSource.includes('Vietcetera')}]" @click="clickSource('Vietcetera')">
		<el-descriptions-item min-width="120">
			<template #label>
				<div><el-icon><user /></el-icon>Trang</div>
			</template>
			Vietcetera
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div><el-icon><iphone /></el-icon>Link</div>
			</template>
			<a href="https://vietcetera.com/" target="blank">https://vietcetera.com/</a>
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div><el-icon><tickets /></el-icon>Giới thiệu</div>
			</template>
			Vietcetera là một nền tảng truyền thông và cộng đồng trực tuyến tại Việt Nam, tập trung vào việc cung cấp thông tin về văn hóa, kinh doanh, và cuộc sống đương đại. Với các bài viết, video và sự kiện đa dạng, Vietcetera nhằm mục tiêu kết nối và chia sẻ thông tin giữa các thế hệ và khám phá những xu hướng mới.
		</el-descriptions-item>
	</el-descriptions>

	<el-descriptions :column="2" border :class="['mb-5', {'selectedSource': selectedSource.includes('Dantri')}]" @click="clickSource('Dantri')">
		<el-descriptions-item min-width="120">
			<template #label>
				<div><el-icon><user /></el-icon>Trang</div>
			</template>
			Dantri
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div><el-icon><iphone /></el-icon>Link</div>
			</template>
			<a href="https://dantri.com.vn/" target="blank">https://dantri.com.vn/</a>
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div><el-icon><tickets /></el-icon>Giới thiệu</div>
			</template>
			Dân trí là một trong những trang tin tức trực tuyến hàng đầu tại Việt Nam. Với nền tảng đa phương tiện, Dantri cung cấp cho độc giả các tin tức chính thống, đa dạng về các lĩnh vực như chính trị, kinh tế, xã hội, giáo dục, và văn hóa. Dantri cũng đặc biệt chú trọng vào việc cung cấp thông tin nhanh chóng, chính xác và đáng tin cậy, đồng thời mang đến những bài viết chất lượng và phản ánh sâu sắc về các vấn đề quan trọng trong xã hội.
		</el-descriptions-item>
	</el-descriptions>

	<el-descriptions :column="2" border :class="['mb-5', {'selectedSource': selectedSource.includes('Vnexpress')}]" @click="clickSource('Vnexpress')">
		<el-descriptions-item min-width="120">
			<template #label>
				<div><el-icon><user /></el-icon>Trang</div>
			</template>
			Vnexpress
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div><el-icon><iphone /></el-icon>Link</div>
			</template>
			<a href="https://vnexpress.net/" target="blank">https://vnexpress.net/</a>
		</el-descriptions-item>

		<el-descriptions-item>
			<template #label>
				<div><el-icon><tickets /></el-icon>Giới thiệu</div>
			</template>
			VnExpress là một trang web tin tức hàng đầu tại Việt Nam, cung cấp thông tin đa dạng về tin tức, kinh doanh, thể thao, giải trí và nhiều lĩnh vực khác. Với chất lượng bài viết chuyên nghiệp và đội ngũ nhân viên giàu kinh nghiệm, VnExpress đáp ứng nhu cầu cập nhật thông tin nhanh chóng, chính xác và đáng tin cậy của người đọc.
		</el-descriptions-item>
	</el-descriptions>
</template>

<script lang="ts">
import {Options, Vue} from 'vue-class-component';

@Options({
	data() {
    return {
			selectedSource: [],
		}
	},

	methods: {
		clickSource(source: string){
			if (this.selectedSource.includes(source))
				this.selectedSource = this.selectedSource.filter((name: any) => name !== source);
			else
				this.selectedSource.push(source)
			
			this.$emit('source-selected', this.selectedSource);
		}
	}
})

export default class SourceSection extends Vue {}
</script>

<style lang="scss" scoped>
.selectedSource{
	border: 2px solid #121212;
}
</style>

