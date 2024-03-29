import pickle
from django.db.models import Q, Case, When
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from api_post.models import PostVector, Posts
from django.db.models import Q, Avg
from api_post.constants import PostStatus
from django.core.files.storage import default_storage
import uuid


def get_recommendations(post_id, category, num_recommendations=5):
    # # Load dữ liệu TruncatedSVD vector từ disk
    # try:
    #     file_name = 'tfidf_vectors.pkl'
    #     file = default_storage.open(file_name, 'rb')
    #     # Read the file content as bytes
    #     file_content = file.read()
    #     # Load the data from the file content
    #     tfidf_vectors_svd = pickle.loads(file_content)
    # except FileNotFoundError:
    #     print("Error: The file does not exist.")
    # except Exception as e:
    #     print("An error occurred while loading the file:", str(e))
    try:
        # Get tất cả vector và post id từ postvector
        post_vectors = PostVector.objects.filter(post__category=category).values_list('vector', 'post_id')
        post_id_dict = [np.frombuffer(vector_pos, dtype=np.float64) for vector_pos, post_id in post_vectors]
        # retrieve bài post đang đọc và convert nó về lại vector
        matrix = np.array(post_id_dict)
        # Tạo một dict để map giữ vector và post id
        post_id_dict = {vector_pos: post_id for vector_pos, post_id in post_vectors}
        # retrieve bài post đang đọc và convert nó về lại vector
        post_vector = PostVector.objects.get(post_id=post_id).vector
        post_vector = np.frombuffer(post_vector, dtype=np.float64)
        # Tính cosine similarities giữ vector bài post hiện tại và các vector của tất cả các bài báo
        similarities = cosine_similarity(post_vector.reshape(1, -1), matrix)
        # Sắp xếp các bài post dựa trên similarities và get ra index các bài post có similarities cao nhất
        top_indices = similarities.argsort()[0][-20:]
        # get vector dựa trên index và convert nó về kiểu byte
        vector = [matrix[index].astype(np.float64).tobytes() for index in top_indices]
        # lấy ra các id của bài post dựa trên vector
        recommended_ids = [post_id_dict.get(index) for index in vector[::-1]]
        try:
            recommended_ids.remove(post_id)
        except:
            pass
        # Get du lieu recomend với status là published and ordered by recommended_ids
        recommended_posts = Posts.objects.filter(
            Q(id__in=recommended_ids) & Q(status=PostStatus.PUBLISHED.value)
        ).prefetch_related('category').prefetch_related('source').prefetch_related('post_rating').annotate(
            avg_rating=Avg("post_rating__star_rating")).order_by(
            Case(*[When(id=id_val, then=pos) for pos, id_val in enumerate(recommended_ids)]))[:num_recommendations]
    except:
        recommended_posts = []
    return recommended_posts

