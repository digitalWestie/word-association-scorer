import subprocess
from pprint import pprint

stopwords = ['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', 'her', 'hers', 'herself', 'it', 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', 'should', 'now']
word2vec_distance = '/home/digitalwestie/Code/word2vec/bin/distance'
word2vec_vector = '/home/digitalwestie/Code/word2vec/data/text8-vector.bin'


def remove_stopwords(arr):
  return set(arr) - set(stopwords)


def get_close_words(word):
  proc = subprocess.Popen([word2vec_distance+' '+word2vec_vector+'<< EOD\n'+word+'\nEXIT\nEOD'], stdout=subprocess.PIPE, shell=True)
  (out, err) = proc.communicate()
  result_set = out.split('------------------------------------------------------------------------')
  if (len(result_set) == 1):
    return []
  result_set = result_set[1]
  lines = result_set.split('\n')
  close_words = []
  for line in lines:
    line = line.split('\t\t')
    if (len(line) == 2):
      close_words.append(line[0].strip())
  return close_words


def build_category_associated():
  associated = {}
  for category in categories:
    associated[category] = get_close_words(category)
    associated[category].append(category)
  return associated


def count_associated(arr1, arr2):
  return len(set(arr1) & set(arr2))


def analyse_text(text, category):
  text = text.strip().lower()
  text.replace('/', ' ').replace('.', '').replace('!', '')
  text_arr = text.split(' ')
  remove_stopwords(text_arr)
  counts = []
  category_words = associated[category]
  for word in text_arr:
    result = get_close_words(word)
    counts.append(count_associated(category_words, result))
  return sum(counts)


def examine(text):
  for category in categories:
    score = analyse_text(text,category)
    print category+": " + str(score)



######

# categories = ["art", "fair", "music", "walk", "charity", "business", "family", "countryside", "craft", "dance", "design", "education", "film", "health", "heritage"]

# associated = build_category_associated()

# text = 'Join scientists from the University of Oxford on an explosive, interactive tour of the science behind atom smashers. This award-winning show is packed with hair-raising demonstrations, explosions and real particle beams.'

# analyse_text(text, 'art')