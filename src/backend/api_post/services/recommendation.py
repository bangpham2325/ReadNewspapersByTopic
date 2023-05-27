import pickle

import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from api_post.models import PostVector, Posts
from django.db.models import Q
from api_post.constants import PostStatus


def get_recommendations(post_id, num_recommendations=5):
    # Load dữ liệu TruncatedSVD vector từ disk
    with open('tfidf_vectors.pkl', 'rb') as file:
        tfidf_vectors_svd = pickle.load(file)
    # Get tất cả vector và post id từ postvector
    post_vectors = PostVector.objects.values_list('vector', 'post_id')
    # Tạo một dict để map giữ vector và post id
    post_id_dict = {vector_pos: post_id for vector_pos, post_id in post_vectors}
    # retrieve bài post đang đọc và convert nó về lại vector
    post_vector = PostVector.objects.get(post_id=post_id).vector
    post_vector = np.frombuffer(post_vector, dtype=np.float64)
    # Tính cosine similarities giữ vector bài post hiện tại và các vector của tất cả các bài báo
    similarities = cosine_similarity(post_vector.reshape(1, -1), tfidf_vectors_svd)
    # Sắp xếp các bài post dựa trên similarities và get ra index các bài post có similarities cao nhất
    top_indices = similarities.argsort()[0][-num_recommendations:]
    # get vector dựa trên index và convert nó về kiểu byte
    vector = [tfidf_vectors_svd[index].astype(np.float64).tobytes() for index in top_indices]
    # lấy ra các id của bài post dựa trên vector
    recommended_ids = [post_id_dict.get(index) for index in vector[::-1]]

    recommended_post = Posts.objects.filter(Q(id__in=recommended_ids) & Q(Q(status=PostStatus.PUBLISHED.value)))

    return recommended_post

