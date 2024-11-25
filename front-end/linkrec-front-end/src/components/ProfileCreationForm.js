import { Link } from "react-router-dom";

function ProfileCreationForm() {
  return (
    <div class="flex items-center justify-center p-14 dark:bg-gray-900 text-white">
      <div class="mx-auto w-full max-w-[550px] bg-white dark:bg-gray-900">
        <form>
          <div class="mb-5">
            <label for="title" class="mb-3 block text-2xl font-medium ">
              Create your profile
            </label>
            <label for="name" class="mb-3 block text-base font-medium ">
              Full Name
            </label>
            <input
              type="text"
              name="name"
              id="name"
              placeholder="Full Name"
              class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            />
          </div>
          <div class="mb-5">
            <label for="webpage" class="mb-3 block text-base font-medium ">
              Webpage
            </label>
            <input
              type="text"
              name="webpage"
              id="webpage"
              placeholder="Enter your website"
              class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            />
          </div>
          <div class="mb-5">
            <label for="email" class="mb-3 block text-base font-medium ">
              Email Address
            </label>
            <input
              type="email"
              name="email"
              id="email"
              placeholder="Enter your email"
              class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
            />
          </div>
          <div class="mb-0 pt-3">
            <label class="mb-5 block text-base font-semibold  sm:text-xl">
              Address Details
            </label>
            <div class="-mx-3 flex flex-wrap">
              <div class="w-full px-3 sm:w-1/2">
                <div class="mb-5">
                  <input
                    type="text"
                    name="area"
                    id="area"
                    placeholder="Enter area"
                    class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                  />
                </div>
              </div>
              <div class="w-full px-3 sm:w-1/2">
                <div class="mb-5">
                  <input
                    type="text"
                    name="city"
                    id="city"
                    placeholder="Enter city"
                    class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                  />
                </div>
              </div>
              <div class="w-full px-3 sm:w-1/2">
                <div class="mb-5">
                  <input
                    type="text"
                    name="state"
                    id="state"
                    placeholder="Enter state"
                    class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                  />
                </div>
              </div>
              <div class="w-full px-3 sm:w-1/2">
                <div class="mb-5">
                  <input
                    type="text"
                    name="post-code"
                    id="post-code"
                    placeholder="Post Code"
                    class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
                  />
                </div>
              </div>
            </div>
          </div>
          <div class="mb-5 pt-3">
            <label class="mb-5 block text-base font-semibold  sm:text-xl">
              Education Details
            </label>
            <div class="mb-5">
              <label for="school" class="mb-3 block text-base font-medium ">
                School
              </label>
              <input
                type="text"
                name="school"
                id="school"
                placeholder="Enter your school"
                class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
              />
            </div>
            <div class="mb-5">
              <label for="degree" class="mb-3 block text-base font-medium ">
                Degree
              </label>
              <input
                type="text"
                name="degree"
                id="degree"
                placeholder="Degree in ..."
                class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
              />
            </div>
            <div class="mb-5">
              <label for="prof-exp" class="mb-3 block text-base font-medium ">
                Professional Experience
              </label>
              <input
                type="text"
                name="prof-exp"
                id="prof-exp"
                placeholder="Relevant professional experience"
                class="w-full rounded-md border border-[#e0e0e0] bg-white py-3 px-6 text-base font-medium text-[#6B7280] outline-none focus:border-[#6A64F1] focus:shadow-md"
              />
            </div>
          </div>

          <div>
            <button class="hover:shadow-form w-full rounded-md bg-[#6A64F1] py-3 px-8 text-center text-base font-semibold text-white outline-none">
              Create Profile
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}

export default ProfileCreationForm;
