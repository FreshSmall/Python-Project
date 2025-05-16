from openai import OpenAI
from dotenv import load_dotenv
load_dotenv()

client = OpenAI()


def kotlin_to_java(input):
    completion = client.chat.completions.create(
        model="deepseek/DeepSeek-R1",
        messages=[
            {"role": "system","content": "把Kotlin 代码转换成 Java 代码。要输出完整的java代码"},
            {"role": "user", "content": f"{input}"}
        ],
        stream=False
    )
    print(completion.choices[0].message.reasoning_content)
    return completion.choices[0].message.content

# Please install OpenAI SDK first: `pip3 install openai`




if __name__ == '__main__':
    input = '''
    package com.baijia.tmk.service.mark

import com.baijia.tmk.common.enums.FieldTypeEnum
import com.baijia.tmk.service.entity.CommonMarkRecordEntity
import com.baijia.tmk.service.entity.FormStyleEntity
import com.baijia.tmk.service.entity.MarkFieldEntity
import com.baijia.tmk.service.mark.MarkDynamicEntity.Companion.COLLECTION_NAME
import com.baijia.tmk.service.mark.MarkDynamicEntity.Companion.DATA_FIELD
import com.baijia.tmk.service.mark.MarkDynamicEntity.Companion.MARK_ID_FIELD
import com.baijia.tmk.service.mark.MarkDynamicEntity.Companion.SCENE_ID_FIELD
import com.baijia.tmk.service.mark.MarkDynamicEntity.Companion.TASK_ID_FIELD
import com.baijia.tmk.service.service.MarkFieldService
import com.baijia.tmk.service.service.SceneService
import org.springframework.data.mongodb.core.MongoTemplate
import org.springframework.data.mongodb.core.query.Criteria
import org.springframework.data.mongodb.core.query.Query
import org.springframework.data.mongodb.core.query.Update
import org.springframework.stereotype.Service
import java.math.BigDecimal
import java.math.RoundingMode

@Service
class MarkDynamicService(val mongoTemplate: MongoTemplate,
    val markFieldService: MarkFieldService, val sceneService: SceneService) {


    fun findByMarkId(markId: Long): Map<String, Any> {
        val query = Query.query(Criteria.where(MARK_ID_FIELD).`is`(markId))
        val dynamicMark = mongoTemplate.findOne(query, MarkDynamicEntity::class.java)
        return dynamicMark?.data ?: mutableMapOf()
    }
}
    '''
    print(kotlin_to_java(input))
