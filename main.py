import asyncio
from configs.docker_utils import start_docker,stop_docker
from Teams.dsa_team import get_team
from autogen_agentchat.messages import TextMessage
from autogen_agentchat.base import TaskResult

async def main():
    team,docker = get_team()
    await start_docker(docker)
    try:
        # Example LeetCode-style problem with starter code and test cases
        task = """
        Find Median of Two Sorted Arrays
        
        Given two sorted arrays nums1 and nums2 of size m and n respectively, return the median of the two sorted arrays.
        
        The overall run time complexity should be O(log (m+n)).
        
        Example 1:
        Input: nums1 = [1,3], nums2 = [2]
        Output: 2.00000
        Explanation: merged array = [1,2,3] and median is 2.
        
        Example 2:
        Input: nums1 = [1,2], nums2 = [3,4]
        Output: 2.50000
        Explanation: merged array = [1,2,3,4] and median is (2 + 3) / 2 = 2.5.
        
        Here's the starter code:
        
        ```python
        class Solution(object):
            def findMedianSortedArrays(self, nums1, nums2):
               
                :type nums1: List[int]
                :type nums2: List[int]
                :rtype: float
                
        ```
        
        Test cases to use:
        1. nums1 = [1,3], nums2 = [2] → Expected output: 2.0
        2. nums1 = [1,2], nums2 = [3,4] → Expected output: 2.5
        3. nums1 = [], nums2 = [1] → Expected output: 1.0
        4. nums1 = [2], nums2 = [] → Expected output: 2.0
        5. nums1 = [1,3,5,7,9], nums2 = [2,4,6,8,10] → Expected output: 5.5
        
        Please implement this solution.
        """
        
        async for message in team.run_stream(task=task):
                if isinstance(message, TextMessage):
                    print('==' * 20)
                    print(message.source, ":::::", message.content)
                elif isinstance(message, TaskResult):
                    print("Stop Reason:", message.stop_reason)
    except Exception as e:
        print(e)

    finally:
        await stop_docker(docker)

if __name__ =="__main__":
    asyncio.run(main())